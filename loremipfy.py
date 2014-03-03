#!/usr/bin/python
import re
import StringIO
import argparse
import google_translate_api as api

def getValues(input):
	fileContent = input.read();
	input.close()

	values = []
	header = fileContent.split("\n", 3);
	for i in xrange(len(header)-1):
		# Excel format
		if re.search("Workbook", header[i]):
			#for match in re.finditer('<Row[^>]*><Data[^>]*>(?P<key>.+)</Data>.*<Data[^>]*>(?P<value>.+)</Data>[\s]*</Cell>[\s]*</Row>', fileContent, re.MULTILINE|re.DOTALL):
			for match in re.finditer('<Row[^>]*>[\s]*<Cell[^>]*><Data[^>]*>(?P<key>[^<]+)</Data>[\s]*</Cell>[\s]*<Cell[^>]*><Data[^>]*>(?P<content>[^<]+)</Data>[\s]*</Cell>[\s]*</Row>', fileContent, re.MULTILINE|re.DOTALL):
				values.append((match.group("key"), match.group('content')))
		# GRAR format
		elif re.search("Localisation", header[i]):
			for match in re.finditer('<key>(?P<key>.*)</key>[\s]*<value>(<!\[CDATA\[)?(?P<content>[^\]<]*)(\]\]>)?</value>', fileContent, re.MULTILINE):
				values.append((match.group("key"), match.group('content')))
		# XLIFF format
		elif re.search("xliff", header[i]):
			pass

	return values

def loremipfy(input, output):
	lorem = list("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque ac lobortis lorem, hendrerit lobortis ligula. In ultricies rutrum ante, ac aliquet lorem. Sed venenatis tellus vel nunc posuere imperdiet. Fusce nulla sem, laoreet vitae dictum ut, iaculis id augue. Vivamus viverra eros quam, eget dictum lacus suscipit nec. Curabitur a mauris turpis. Nullam at laoreet justo. Aenean a diam eget odio luctus rhoncus. Fusce blandit pharetra semper. Vivamus posuere, lectus ac lacinia molestie, velit velit blandit ante, ut luctus elit justo quis nisl. Etiam magna lectus, sagittis et odio quis, porta cursus metus. Nullam quis urna pharetra purus gravida elementum. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec malesuada dictum consectetur. ")

	fileContent = input.read();
	input.close()
	outputString = StringIO.StringIO()
	prevEnd = 0

	for match in re.finditer('<value>(<!\[CDATA\[)?(?P<content>[^\]<]*)(\]\]>)?</value>', fileContent, re.MULTILINE):
	    content = list(match.group('content'))
	    for i in xrange(len(content)):
	    	if(content[i] != '\n'):
	    		content[i] = lorem[i]
	    outputString.write(fileContent[prevEnd:match.start()] + '<value><![CDATA[' + "".join(content) + ']]></value>')
	    prevEnd = match.end()
	    
	outputString.write(fileContent[prevEnd:])
	output.write(outputString.getvalue()+"\n")
	output.close()

def excelsior(input, output):
	if not args.template:
		print "You must specify an Excel template (-t FILE or --template FILE)"
	else:
		excelTemplate = args.template.read()
		match = re.search(r'(<Row.*)(?P<key>key)(.*)(?P<value>value)(.*</Row>)', excelTemplate, flags=re.MULTILINE|re.DOTALL)
		if not match:
			print "Unable to match template. Are you sure the file is correct?"
		else:
			outputString = StringIO.StringIO();
			outputString.write(excelTemplate[:match.start()])
			localeList = getValues(input)
			for key, value in localeList:
				outputString.write(match.group(1))
				outputString.write(key)
				outputString.write(match.group(3))
				if args.language:
					src = translator.detect(value)
					translated = translator.trans_sentence(src, args.language, value)
					outputString.write(translated)
				else:
					outputString.write(value)
				outputString.write(match.group(5))
			outputString.write(excelTemplate[match.end():]) #.decode("utf8")
			bufferValue = outputString.getvalue()+"\n"
			bufferValue = bufferValue.replace('ss:ExpandedRowCount="1"', 'ss:ExpandedRowCount="'+str(len(localeList))+'"')
			output.write(bufferValue)#.encode('utf8')
			outputString.close()
			output.close()

def xmlify(input, output):
	outputString = StringIO.StringIO();
	outputString.write("<?xml version='1.0'?>\n<Localisation>");
	for key, value in getValues(input):
	 	outputString.write("<Element>\n\t<key>"); 
	 	outputString.write(key); 
	 	outputString.write("</key>\n\t<value><![CDATA["); 
	 	outputString.write(value); 
	 	outputString.write("]]></value>\n</Element>\n"); 
	outputString.write("</Localisation");
	output.write(outputString.getvalue());
	outputString.close();
	output.close();

# Start	
parser = argparse.ArgumentParser(description='Transform a localisation file')
parser.add_argument('input', metavar='input_file', type=argparse.FileType('r'), help='input file to transform')
parser.add_argument('-l', '--lorem', dest='lorem_output', action='store', type=argparse.FileType('w'), help='Replace all the content by a Lorem Ipsum extract')
parser.add_argument('-e', '--excel', dest='excel_output', action='store', type=argparse.FileType('w'), help='Convert the location file into an MS Excel file')
parser.add_argument('-x', '--xml', dest='xml_output', action='store', type=argparse.FileType('w'), help='Convert the location file into an XML file')
parser.add_argument('-t', '--template', dest='template', action='store', type=argparse.FileType('r'), help='Excel Template for Excel export')
parser.add_argument('--lang', dest='language', action='store', help='Language location will be translated to')
args = parser.parse_args()

if args.language:
	translator = api.TranslateService()
if args.lorem_output:
	loremipfy(args.input, args.lorem_output)
elif args.excel_output:
	excelsior(args.input, args.excel_output)
elif args.xml_output:
	xmlify(args.input, args.xml_output)

# Futur TTS ?
#tts = api.TTSService()
#import subprocess
#import tempfile
#with tempfile.NamedTemporaryFile() as f:
#	data = tts.get_mpeg_binary('en', 'This is a sentence.')
#	f.write(data)
#	subprocess.call(['afplay', f.name])