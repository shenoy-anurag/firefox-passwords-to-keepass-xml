import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement
from io import BytesIO


class StringElement:
    TAG = 'String'
    KEY = 'Key'
    VALUE = 'Value'

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def create_element(self):
        el = Element(self.TAG)
        s1 = SubElement(el, self.KEY)
        s1.text = self.key
        s2 = SubElement(el, self.VALUE)
        s2.text = self.value
        return el


class Entry:
    TAG = 'Entry'

    TITLE = 'title'
    USERNAME = 'username'
    PASSWORD = 'password'
    URL = 'url'
    NOTES = 'notes'
    ATTRIBUTES = [TITLE, USERNAME, PASSWORD, URL, NOTES]
    SUB_ELEMENT_KEYS = {TITLE: 'Title', USERNAME: 'UserName', PASSWORD: 'Password', URL: 'URL', NOTES: 'Notes'}

    def __init__(self, title, username, password, url, notes=None):
        if not title:
            raise Exception("title of entry missing")
        if not username:
            raise Exception("username of entry missing")
        if not password:
            raise Exception("password of entry missing")
        self.__setattr__(self.TITLE, title)
        self.__setattr__(self.USERNAME, username)
        self.__setattr__(self.PASSWORD, password)
        self.__setattr__(self.URL, url if notes else '')
        self.__setattr__(self.NOTES, notes if notes else '')
        self.el = Element(self.TAG)
        self.added_elements = set()

    def create_element(self):
        for attr in self.ATTRIBUTES:
            if attr not in self.added_elements:
                attr_val = self.__getattribute__(attr)
                str_el = StringElement(key=self.SUB_ELEMENT_KEYS[attr], value=attr_val)
                xml_el = str_el.create_element()
                self.el.append(xml_el)
                self.added_elements.add(attr)

    def generate_xml(self):
        bytes_buffer = BytesIO()
        tree = ET.ElementTree(self.el)
        tree.write(bytes_buffer)
        return bytes_buffer.getvalue()


def create_test_entry():
    sample_entry = Entry(
        title='Test 1', username='test.subject@example.com', password='password1', url='https://accounts.example.com',
        notes='Lorem ipsum'
    )
    sample_entry.create_element()
    xml_str = sample_entry.generate_xml()
    return xml_str


if __name__ == "__main__":
    # test entry creation
    xml_entry = create_test_entry()
    print(xml_entry.decode())
    file_path = '../exp/created_entry.xml'
    with open(file_path, "wb") as f:
        f.write(xml_entry)
