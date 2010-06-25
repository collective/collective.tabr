from zope.component import getUtility

from Products.TinyMCE.interfaces.utility import ITinyMCE

from Products.CMFCore.utils import getToolByName

STYLES = (
    ('Tab', 'h2', 'content-tab'),
    ('Default Tab', 'h2', 'default-content-tab'),
    ('Pane Break', 'hr', 'pane-break'),
)

FCKTEMPLATE = """
<Style name="%s" element="%s">
  <Attribute name="class" value="%s" />
</Style>"""

def importVarious(context):
    # Only run step if a flag file is present
    log = context.getLogger('collective.tabr')
    if context.readDataFile('tabr_various.txt') is None:
        return
    
    site = context.getSite()

    tinymce = getUtility(ITinyMCE)
    if tinymce:
        tinymce.styles += u'\n'+u'\n'.join([u'|'.join(style) for style in STYLES])
        log.info("TinyMCE Styles Added")
        
    kupu = getToolByName(site, 'kupu_library_tool', None)
    if kupu is not None:
        all_styles = kupu.getParagraphStyles()
        for style in STYLES:
            all_styles += ('|'.join(style),)
        kupu.configure_kupu(parastyles= all_styles)
        log.info("Kupu styles added")
    
    portal_props = getToolByName(site, 'portal_properties')
    fck_props = getattr(portal_props, 'fckeditor_properties', None)
    if fck_props is not None:
        all_styles = fck_props.getProperty('fck_menu_styles', None)
        for style in STYLES:
            all_styles += FCKTEMPLATE % style
        fck_props.manage_changeProperties(fck_menu_styles= all_styles)
        log.info("FCKEditor styles added")
        
    return 'Styles added'
    