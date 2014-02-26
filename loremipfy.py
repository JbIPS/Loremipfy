#!/usr/bin/python
import re
from cStringIO import StringIO
import argparse

def getValues(input):
	fileContent = input.read();

	values = []
	for match in re.finditer('<key>(?P<key>.*)</key>[\s]*<value>(<!\[CDATA\[)?(?P<content>[^\]<]*)(\]\]>)?</value>', fileContent, re.MULTILINE):
		values.append((match.group("key"), match.group('content')))
	return values

def loremipfy(input, output):
	lorem = list("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque ac lobortis lorem, hendrerit lobortis ligula. In ultricies rutrum ante, ac aliquet lorem. Sed venenatis tellus vel nunc posuere imperdiet. Fusce nulla sem, laoreet vitae dictum ut, iaculis id augue. Vivamus viverra eros quam, eget dictum lacus suscipit nec. Curabitur a mauris turpis. Nullam at laoreet justo. Aenean a diam eget odio luctus rhoncus. Fusce blandit pharetra semper. Vivamus posuere, lectus ac lacinia molestie, velit velit blandit ante, ut luctus elit justo quis nisl. Etiam magna lectus, sagittis et odio quis, porta cursus metus. Nullam quis urna pharetra purus gravida elementum. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec malesuada dictum consectetur. ")

	fileContent = input.read();
	outputString = StringIO()
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

def excelsior(input, output):
	if not args.template:
		print "You must specify an Excel template (-t FILE or --template FILE)"
	else:
		outputString = StringIO()
		excelTemplate = args.template.read()
		match = re.search(r'(<Row.*)(?P<key>key)(.*)(?P<value>value)(.*</Row>)', excelTemplate, flags=re.MULTILINE|re.DOTALL)
		if not match:
			print "mort"
		else:
			outputString.write(excelTemplate[:match.start()])
			localeList = getValues(input)
			for key, value in localeList:
				outputString.write(match.group(1))
				outputString.write(key)
				outputString.write(match.group(3))
				outputString.write(value)
				outputString.write(match.group(5))
			outputString.write(excelTemplate[match.end():])
		bufferValue = outputString.getvalue()+"\n"
		bufferValue = bufferValue.replace('ss:ExpandedRowCount="1"', 'ss:ExpandedRowCount="'+str(len(localeList))+'"')
		output.write(bufferValue)

# Start	
parser = argparse.ArgumentParser(description='Transform a localisation file')
parser.add_argument('input', metavar='file', type=argparse.FileType('r'), help='input file to transform')
parser.add_argument('-l', '--lorem', dest='lorem_output', action='store', type=argparse.FileType('w'), help='Replace all the content by a Lorem Ipsum extract')
parser.add_argument('-e', '--excel', dest='excel_output', action='store', type=argparse.FileType('w'), help='Convert the XML location file into an MS Excel file')
parser.add_argument('-t', '--template', dest='template', action='store', type=argparse.FileType('r'), help='Excel Template for Excel export')

args = parser.parse_args()
if args.lorem_output:
	loremipfy(args.input, args.lorem_output)
elif args.excel_output:
	excelsior(args.input, args.excel_output)