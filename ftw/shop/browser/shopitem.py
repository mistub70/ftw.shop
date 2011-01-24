import transaction
from decimal import Decimal
from Products.CMFCore.utils import getToolByName
import simplejson

from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getUtility

from ftw.shop import shopMessageFactory as _
from ftw.shop.interfaces import IVariationConfig


class ShopItemView(BrowserView):
    """Default view for a shop item
    """

    __call__ = ViewPageTemplateFile('templates/shopitem.pt')

    single_item_template = ViewPageTemplateFile('templates/listing/single_item.pt')
    one_variation_template = ViewPageTemplateFile('templates/listing/one_variation.pt')
    two_variations_template = ViewPageTemplateFile('templates/listing/two_variations.pt')

    def getItems(self):
        """Returns a list with this item as its only element,
        so the listing viewlet can treat it like a list of items
        """
        context = aq_inner(self.context)
        return [context]

    def single_item(self, item):
        return self.single_item_template(item=item)

    def one_variation(self, item):
        return self.one_variation_template(item=item)

    def two_variations(self, item):
        return self.two_variations_template(item=item)

    def getItemDatas(self):
        """Returns a dictionary of an item's properties to be used in
        templates. If the item has variations, the variation config is
        also included.
        """
        results = []
        for item in self.getItems():
            assert(item.portal_type == 'ShopItem')
            varConf = IVariationConfig(item)

            has_variations = varConf.hasVariations()

            image = None
            tag = None
            if has_variations:
                skuCode = None
                price = None
            else:
                varConf = None
                skuCode = item.Schema().getField('skuCode').get(item)
                price = item.Schema().getField('price').get(item)

            if image:
                tag = image.tag(scale='tile')

            results.append(dict(title = item.Title(),
                                description = item.Description(),
                                url = item.absolute_url(),
                                imageTag = tag,
                                variants = None,
                                skuCode = skuCode,
                                price = price,
                                uid = item.UID(),
                                varConf = varConf,
                                hasVariations = has_variations))
        return results

    def getVariationsConfig(self):
        """Returns the variation config for the item currently being viewed
        """
        context = aq_inner(self.context)
        variation_config = IVariationConfig(context)
        return variation_config

    def getVarDictsJSON(self):
        """Returns a JSON serialized dict with UID:varDict pairs, where UID
        is the ShopItem's UID and varDict is the item's variation dict.
        This is being used for the compact category view where inactive
        item variations must not be buyable.
        """
        varDicts = {}
        items = self.getItemDatas()
        for item in items:
            uid = item['uid']
            varConf = item['varConf']
            if varConf is not None:
                varDicts[uid] = dict(varConf.getVariationDict())
            else:
                varDicts[uid] = {}

            # Convert Decimals to Strings for serialization
            varDict = varDicts[uid]
            for vcode in varDict.keys():
                i = varDict[vcode]
                for k in i.keys():
                    val = i[k]
                    if isinstance(val, Decimal):
                        val = str(val)
                        i[k] = val

        return simplejson.dumps(varDicts)


class ShopCompactItemView(ShopItemView):
    """Compact view for a shop item
    """

    one_variation_template = ViewPageTemplateFile('templates/listing/one_variation_compact.pt')
    two_variations_template = ViewPageTemplateFile('templates/listing/two_variations_compact.pt')


class EditVariationsView(BrowserView):
    """View for editing ShopItem Variations
    """
    template = ViewPageTemplateFile('templates/edit_variations.pt')

    def __call__(self):
        """
        Self-submitting form that displays ShopItem Variations
        and updates them

        """
        form = self.request.form

        # Make sure we had a proper form submit, not just a GET request
        submitted = form.get('form.submitted', False)
        if submitted:
            variation_config = IVariationConfig(self.context)

            attributes, edited_var_data = self._parse_edit_variations_form()
            v1attr = attributes[0].keys()[0]
            v2attr = attributes[1].keys()[0]
            v1values = attributes[0][v1attr]
            v2values = attributes[1][v2attr]

            self.context.Schema().getField('variation1_attribute').set(self.context, v1attr)
            self.context.Schema().getField('variation2_attribute').set(self.context, v2attr)
            self.context.Schema().getField('variation1_values').set(self.context, v1values)
            self.context.Schema().getField('variation2_values').set(self.context, v2values)

            variation_config.updateVariationConfig(edited_var_data)

            IStatusMessage(self.request).addStatusMessage(
                _(u'msg_variations_saved',
                  default=u"Variations saved."), type="info")
            self.request.RESPONSE.redirect(self.context.absolute_url())

        return self.template()

    def _parse_edit_variations_form(self):
        """Parses the form the user submitted when editing variations,
        and returns a dictionary that contains the variation data.
        """
        form = self.request.form
        variation_config = IVariationConfig(self.context)
        variation_data = {}

        def _parse_data(variation_code):
            data = {}
            data['active'] = bool(form.get("%s-active" % variation_code))
            # TODO: Handle decimal more elegantly
            price = form.get("%s-price" % variation_code)
            try:
                p = int(price)
                # Create a tuple of ints from string
                digits = tuple([int(i) for i in list(str(p))]) + (0, 0)
                data['price'] = Decimal((0, digits, -2))
            except ValueError:
                if not price == "":
                    data['price'] = Decimal(price)
                else:
                    data['price'] = Decimal("0.00")

            data['skuCode'] = form.get("%s-skuCode" % variation_code)
            data['description'] = form.get("%s-description" % variation_code)

            # At this point the form has already been validated,
            # so uniqueness of sku codes is ensured
            data['hasUniqueSKU'] = True
            return data


        if len(variation_config.getVariationAttributes()) == 1:
            # One variation attribute
            for i, var1_value in enumerate(variation_config.getVariation1Values()):
                variation_code = 'var-%s' % i

                variation_data[variation_code] = _parse_data(variation_code)
        else:
            # Two variation attributes
            for i, var1_value in enumerate(variation_config.getVariation1Values()):
                for j, var2_value in enumerate(variation_config.getVariation2Values()):
                    variation_code = 'var-%s-%s' % (i, j) 
                    variation_data[variation_code] = _parse_data(variation_code)

        v1attr = form.get('v1attr')
        v2attr = form.get('v2attr')
        
        v1values = []
        for key in form.keys():
            if 'v1-value-' in key:
                v1values.append(form.get(key))

        v2values = []
        for key in form.keys():
            if 'v2-value-' in key:
                v2values.append(form.get(key))
        
        attributes = [{v1attr:v1values}, {v2attr:v2values}]
        return (attributes, variation_data)

    def getVariationsConfig(self):
        """Returns the variation config for the item being edited
        """
        context = aq_inner(self.context)
        variation_config = IVariationConfig(context)
        return variation_config


class MigrateVariationsView(BrowserView):
    """View to migrate variations of all shop items
    """

    def __call__(self):
        """Migrates all items
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        normalize = getUtility(IIDNormalizer).normalize
        items = catalog(portal_type="ShopItem")

        for item in items:
            obj = item.getObject()
            print obj.Title()

            var_conf = IVariationConfig(obj)
            varAttrs = var_conf.getVariationAttributes()
            num_variations = len(varAttrs)
            if num_variations == 0:
                # No migration needed
                continue

            var_dict = var_conf.getVariationDict()
            if str(type(var_dict)) == "<class 'zc.dict.dict.OrderedDict'>":
                continue

            if num_variations == 2:
                migrated = True
                keys = var_dict.keys()

                for key in keys:
                    try:
                        key = key.replace('var-', '')
                        split_keys = key.split('-')
                        if not len(split_keys) == 2:
                            migrated = False
                            continue
                        a, b = split_keys
                        if not (a.isdigit() and b.isdigit()):
                            migrated = False
                    except:
                        migrated = False

                if obj.Title() == "Unmigrated Item":
                    import pdb; pdb.set_trace( )

                if not migrated:
                    mapping = {}
                    for i, v1 in enumerate(var_conf.getVariation1Values()):
                        for j, v2 in enumerate(var_conf.getVariation2Values()):
                            vkey = normalize("%s-%s" % (v1, v2))
                            vcode = "var-%s-%s" % (i, j)
                            mapping[vkey] = vcode



                    for vkey in mapping.keys():
                        vcode = mapping[vkey]
                        # Store data with new vcode
                        try:
                            var_dict[vcode] = var_dict[vkey]
                            del var_dict[vkey]
                            var_conf.updateVariationConfig(var_dict)
                            transaction.commit()
                        except KeyError:
                            print "Migration of item %s failed!" % obj.Title()

                if num_variations == 1:
                    migrated = True
                    keys = var_dict.keys()
                    for key in keys:
                        key = key.replace('var-', '')
                        if not key.isdigit():
                            migrated = False

                    if not migrated:
                        mapping = {}
                        for i, v1 in enumerate(var_conf.getVariation1Values()):
                            vkey = normalize(v1)
                            vcode = "%s" % i
                            mapping[vkey] = vcode

                        for vkey in mapping.keys():
                            vcode = mapping[vkey]
                            # Store data with new vcode
                            var_dict[vcode] = var_dict[vkey]
                            del var_dict[vkey]
                            var_conf.updateVariationConfig(var_dict)
                            transaction.commit()
        return "Items Migrated"
                

            
        
