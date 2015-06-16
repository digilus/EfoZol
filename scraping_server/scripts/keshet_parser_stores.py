from cStringIO import StringIO
import xml.etree.cElementTree as ET
import sys
import json

def item_text(item,field):
    ret = item.find(field)
    if ret is None: return 'MISSING'
    ret = ret.text
    if ret is None: return 'MISSING'
    return ret

def parse_stores_file(stores_fobj, out_fobj):    
    dom = ET.parse(stores_fobj)
    root = dom.getroot() # If only it would be this simple on an iPhone

    outputdict = {'root': dict()}
    root_dict = outputdict['root']
    root_dict['XmlDocVersion'] = ''
    root_dict['ChainId'] = item_text(root, 'ChainId')
    root_dict['Stores'] = {'store': []}
    stores_arr = root_dict['Stores']['store']
    for subchain in root.find("SubChains"):
        sub_chain_id = item_text(subchain, "SubChainId")
        sub_chain_name = item_text(subchain, "SubChainName")
        for store in subchain.find('Stores'):
            s_dict = {}
            s_dict['SubChainName'] = sub_chain_name
            s_dict['SubChainId'] = sub_chain_id
            fields = [
                "StoreId",     
                "BikoretNo",   
                "StoreType",   
                "ChainName",   
                "StoreName",   
                "Address",     
                "City",        
                "ZipCode"     
            ]
            for field in fields:
                s_dict[field] = item_text(store, field)
            stores_arr.append(s_dict)

    json.dump(outputdict, out_fobj, sort_keys=True, indent=4, separators=(',',': '))

if __name__ == '__main__':
    stores_file = file(sys.argv[1], "rb")
    output_file = file(sys.argv[2], "wb")
    parse_stores_file(stores_file, output_file)



