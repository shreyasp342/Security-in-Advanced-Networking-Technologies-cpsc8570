import requests
import json
#import xml.etree.ElementTree as ET

xmlN1 = '<?xml version="1.0" encoding="UTF-8" standalone="no"?><input xmlns="urn:opendaylight:flow:service"><barrier>false</barrier><node xmlns:inv="urn:opendaylight:inventory">/inv:nodes/inv:node[inv:id="'
xmlN2 = '"]</node>'

xmlDstIP1 = '<ipv4-destination>'
xmlDstIP2 = '/32</ipv4-destination>'

xmlSrcIP1 = '<ipv4-source>'
xmlSrcIP2 = '/32</ipv4-source>'

xmlB1 = '<cookie>55</cookie><flags>SEND_FLOW_REM</flags><hard-timeout>0</hard-timeout><idle-timeout>0</idle-timeout><installHw>false</installHw><match><ethernet-match><ethernet-type><type>2048</type></ethernet-type></ethernet-match>'
xmlB2 = '</match><instructions><instruction><order>0</order><apply-actions><action><order>0</order><drop-action/></action></apply-actions></instruction></instructions><priority>3</priority><strict>false</strict><table_id>0</table_id></input>'

headers = {'Content-Type': 'application/xml'}

SourceIP = raw_input('Source IP: ')
if len(SourceIP) == 0:
	SourceIP = '10.0.0.3'
DestinationIP = raw_input('Destination IP: ')
if len(DestinationIP) == 0:
	DestinationIP = '10.0.0.2'
action = raw_input('Action (allow/deny): ')
if len(action) == 0:
	action = 'deny'

xmlSrcIP = xmlSrcIP1 + SourceIP + xmlSrcIP2
xmlDstIP = xmlDstIP1 + DestinationIP + xmlDstIP2
#print xmlSrcIP
#print xmlDstIP

urlInv = 'http://localhost:8181/restconf/operational/opendaylight-inventory:nodes/'
response = requests.get(urlInv, auth=('admin', 'admin'))

lst = json.loads(response.text)
control = list()
for item in lst['nodes']['node']:
	control.append(item['id'])

for item in control:
	print 'adding ACL Rule to switch ',item,' : ', action, ' packets flowing from ', SourceIP, ' to ', DestinationIP
	xmlNode = xmlN1 + item + xmlN2
	xmlScript = xmlNode + xmlB1 + xmlSrcIP + xmlDstIP + xmlB2
	if action == 'deny':
		requests.post('http://localhost:8080/restconf/operations/sal-flow:add-flow', data=xmlScript, headers=headers, auth=('admin', 'admin'))
	else:
		requests.post('http://localhost:8080/restconf/operations/sal-flow:remove-flow', data=xmlScript, headers=headers, auth=('admin', 'admin'))
#	print xmlScript



#tree = ET.parse(response.text)
#print tree
#root = tree.getroot()
#print root.tag
