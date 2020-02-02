import xmlschema
import lxml.etree as ET


class XMLHandler:
    def __init__(self, xml: str, xsd: str, xslt: str):
        self.path_xml = xml
        self.path_xsd = xsd
        self.path_xslt = xslt
        self.schema, self.xml, self.xslt = None, None, None

    def __read_data__(self):
        self.__read_schema__()
        self.__read_xml__()
        self.__read_xslt__()

    @staticmethod
    def __start_log__():
        with open('log.txt', 'w') as log:
            log.write('Started.\n')

    @staticmethod
    def __to_log__(info: str):
        with open('log.txt', 'a') as log:
            log.write(info)

    def __read_schema__(self):
        try:
            self.schema = xmlschema.XMLSchema(self.path_xsd)
            self.__to_log__('XMLSchema has been successfully read.\n')
        except FileNotFoundError:
            self.__to_log__('XSD file does not exist.\nExit.')
            raise FileNotFoundError('XSD file does not exist.')
        except xmlschema.validators.exceptions.XMLSchemaParseError:
            self.__to_log__('Invalid scheme.\nExit.')
            raise FileNotFoundError('Invalid scheme.')

    def __read_xml__(self):
        try:
            self.xml = ET.parse(self.path_xml)
            self.__to_log__('Input XML has been successfully read.\n')
        except FileNotFoundError:
            self.__to_log__('XML file does not exist.\nExit.')
            raise FileNotFoundError('XML file does not exist.')

    def __read_xslt__(self):
        try:
            self.xslt = ET.parse(self.path_xslt)
            self.__to_log__('XSLT has been successfully read.\n')
        except FileNotFoundError:
            self.__to_log__('XML file does not exist.\nExit.')
            raise FileNotFoundError('XML file does not exist.')

    def __validate__(self, xml_file):
        try:
            self.schema.validate(xml_file)
            self.__to_log__('Input XML file has successfully passed validation.')
        except xmlschema.validators.exceptions.XMLSchemaValidationError:
            self.__to_log__('XML is invalid according to the XSD scheme.\nExit.')
            raise

    def __modify_xml__(self):
        self.__validate__(self.path_xml)
        transform = ET.XSLT(self.xslt)
        new_xml = transform(self.xml)
        self.__validate__(new_xml)
        return new_xml

    def __make_out_file__(self, new_xml):
        with open(input('Enter the path to a new file using its name (.xml):\n'), 'w') as out:
            try:
                new_xml.write(out)
                self.__to_log__('Output file has been successfully created.\nExit.')
            except FileNotFoundError:
                self.__to_log__("The directory doesn't exists.\nExit.")
                raise FileNotFoundError

    def run(self):
        self.__start_log__()
        self.__read_schema__()
        self.__read_xml__()
        self.__read_xslt__()
        new_xml = self.__modify_xml__()
        self.__make_out_file__(new_xml)
