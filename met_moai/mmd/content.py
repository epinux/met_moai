from lxml import etree
import urllib2
import met_moai.mmd.util as util
import logging
import datetime


class MMDContent(object):
    def __init__(self, provider):
        self.provider = provider
        self.id = None
        self.modified = None
        self.deleted = False
        self.sets = {}
        self.metadata = None
        self._ns = {'mmd': 'http://www.met.no/schema/mmd',
              'gml': 'http://www.opengis.net/gml'}

    def _generate_identifier(self, path):
        return unicode(path.split('/')[-1][:-4])

    def _get_sets(self, root):
        ret = {}
        for element in root.xpath('mmd:collection', namespaces=self._ns):
            if element.text:
                text = unicode(element.text)
                ret[text] = {u'name': text,  u'description': text}
        return ret

    def update(self, data):
        logging.info(data['id'])
        self.id = data['id']
        self.modified = data['modified']
        self.deleted = data['deleted']
        document = urllib2.urlopen(data['url']).read()
        root = etree.fromstring(document)
        if root.tag != '{http://www.met.no/schema/mmd}mmd':
            logging.error(data['url'] + ' is an invalid document')
            return
        if not self.deleted:
            parsed_time = root.xpath('mmd:last_metadata_update', namespaces=self._ns)
            if parsed_time:
                self.modified = util.parse_time(parsed_time[0].text)
        metadata_status = root.xpath('mmd:metadata_status',  namespaces=self._ns)
        if metadata_status:
            self.deleted = metadata_status[0].text.strip().lower() != 'active'
        self.sets = self._get_sets(root)
        self.metadata = {'mmd': etree.tostring(root)}
        logging.info(data['id'] + ': ok')
