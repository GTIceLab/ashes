import xml.etree.ElementTree as ET
import os

# Define the input and output file paths
input_xml_path = "rrgraph.xml"
output_xml_path = "rrgraph_modified.xml"

print(f"Loading and parsing the XML file: {input_xml_path}...")

# Ensure the input file exists before proceeding
if not os.path.exists(input_xml_path):
    print(f"Error: The file {input_xml_path} was not found in the current directory.")
    exit()

# Parse the XML file
tree = ET.parse(input_xml_path)
root = tree.getroot()

# Step 1: Catalog CHANX and CHANY nodes with their locations and PTCs
print("Identifying and mapping CHANX and CHANY nodes...")
chan_node_ids = set()

# Dictionaries to quickly look up node IDs by their (x, y, ptc) coordinates
chanx_dict = {}
chany_dict = {}

rr_nodes = root.find('rr_nodes')
if rr_nodes is not None:
    for node in rr_nodes.findall('node'):
        node_type = node.get('type')
        node_id = node.get('id')
        
        if node_type in ('CHANX', 'CHANY'):
            chan_node_ids.add(node_id)
            
            # Extract location details
            loc = node.find('loc')
            if loc is not None:
                xlow = int(loc.get('xlow'))
                xhigh = int(loc.get('xhigh'))
                ylow = int(loc.get('ylow'))
                yhigh = int(loc.get('yhigh'))
                ptc = int(loc.get('ptc'))
                
                # Only map wires where high and low coordinates match (length 1)
                if xlow == xhigh and ylow == yhigh:
                    if node_type == 'CHANX':
                        chanx_dict[(xlow, ylow, ptc)] = node_id
                    elif node_type == 'CHANY':
                        chany_dict[(xlow, ylow, ptc)] = node_id
else:
    print("Error: Could not find the <rr_nodes> section in the XML.")
    exit()

# Step 2: Identify and remove the existing S-block edges
print("Scanning and removing existing CHAN-to-CHAN edges...")
rr_edges = root.find('rr_edges')
edges_removed_count = 0

if rr_edges is not None:
    edges_to_remove = []
    
    for edge in rr_edges.findall('edge'):
        src = edge.get('src_node')
        sink = edge.get('sink_node')
        
        # Check if both source and sink are channel nodes
        if src in chan_node_ids and sink in chan_node_ids:
            edges_to_remove.append(edge)
    
    for edge in edges_to_remove:
        rr_edges.remove(edge)
        edges_removed_count += 1
        
    print(f"Successfully removed {edges_removed_count} edges.")
else:
    print("Error: Could not find the <rr_edges> section in the XML.")
    exit()

# Step 3: Add new one-to-one bidirectional edges (CHANX 0-7 to CHANY 8-15 ABOVE)
print("Pass 1: Adding new edges (CHANX 0-7 to CHANY 8-15 ABOVE)...")
edges_added_count_above = 0

if rr_edges is not None:
    for x in range(0, 11):          
        for y in range(0, 11):      
            for ptc_x in range(0, 8):  
                
                ptc_y = ptc_x + 8
                src_key = (x, y, ptc_x)
                sink_key = (x, y + 1, ptc_y) # Target CHANY is at y + 1 (ABOVE)
                
                if src_key in chanx_dict and sink_key in chany_dict:
                    src_id = chanx_dict[src_key]
                    sink_id = chany_dict[sink_key]
                    
                    new_edge_forward = ET.Element('edge')
                    new_edge_forward.set('src_node', src_id)
                    new_edge_forward.set('sink_node', sink_id)
                    new_edge_forward.set('switch_id', '2')
                    
                    new_edge_backward = ET.Element('edge')
                    new_edge_backward.set('src_node', sink_id)
                    new_edge_backward.set('sink_node', src_id)
                    new_edge_backward.set('switch_id', '2')
                    
                    rr_edges.append(new_edge_forward)
                    rr_edges.append(new_edge_backward)
                    edges_added_count_above += 2

print(f"  -> Pass 1 complete: {edges_added_count_above} edges added.")

# Step 4: Add new one-to-one bidirectional edges (CHANX 0-7 to CHANY 8-15 SAME LEVEL)
print("Pass 2: Adding new edges (CHANX 0-7 to CHANY 8-15 SAME LEVEL)...")
edges_added_count_same_level_8_15 = 0

if rr_edges is not None:
    for x in range(0, 11):          
        for y in range(0, 11):      
            for ptc_x in range(0, 8):  
                
                ptc_y = ptc_x + 8
                src_key = (x, y, ptc_x)
                sink_key = (x, y, ptc_y) # Target CHANY is at the same y level
                
                if src_key in chanx_dict and sink_key in chany_dict:
                    src_id = chanx_dict[src_key]
                    sink_id = chany_dict[sink_key]
                    
                    new_edge_forward = ET.Element('edge')
                    new_edge_forward.set('src_node', src_id)
                    new_edge_forward.set('sink_node', sink_id)
                    new_edge_forward.set('switch_id', '2')
                    
                    new_edge_backward = ET.Element('edge')
                    new_edge_backward.set('src_node', sink_id)
                    new_edge_backward.set('sink_node', src_id)
                    new_edge_backward.set('switch_id', '2')
                    
                    rr_edges.append(new_edge_forward)
                    rr_edges.append(new_edge_backward)
                    edges_added_count_same_level_8_15 += 2

print(f"  -> Pass 2 complete: {edges_added_count_same_level_8_15} edges added.")

# Step 5: Add new one-to-one bidirectional edges (CHANX 0-7 to CHANY 0-7 SAME LEVEL)
print("Pass 3: Adding new edges (CHANX 0-7 to CHANY 0-7 SAME LEVEL)...")
edges_added_count_same_level_0_7 = 0

if rr_edges is not None:
    for x in range(0, 11):          
        for y in range(0, 11):      
            for ptc_x in range(0, 8):  
                
                ptc_y = ptc_x
                src_key = (x, y, ptc_x)
                sink_key = (x, y, ptc_y) # Target CHANY is at the same y level
                
                if src_key in chanx_dict and sink_key in chany_dict:
                    src_id = chanx_dict[src_key]
                    sink_id = chany_dict[sink_key]
                    
                    new_edge_forward = ET.Element('edge')
                    new_edge_forward.set('src_node', src_id)
                    new_edge_forward.set('sink_node', sink_id)
                    new_edge_forward.set('switch_id', '2')
                    
                    new_edge_backward = ET.Element('edge')
                    new_edge_backward.set('src_node', sink_id)
                    new_edge_backward.set('sink_node', src_id)
                    new_edge_backward.set('switch_id', '2')
                    
                    rr_edges.append(new_edge_forward)
                    rr_edges.append(new_edge_backward)
                    edges_added_count_same_level_0_7 += 2

print(f"  -> Pass 3 complete: {edges_added_count_same_level_0_7} edges added.")

# Step 6: Add new one-to-one bidirectional edges (CHANY 0-7 to CHANY 8-15 ABOVE)
print("Pass 4: Adding new edges (CHANY 0-7 to CHANY 8-15 ABOVE)...")
edges_added_count_chany_above = 0

if rr_edges is not None:
    for x in range(0, 11):          
        for y in range(0, 11):      
            for ptc_y1 in range(0, 8):  
                
                ptc_y2 = ptc_y1 + 8
                src_key = (x, y, ptc_y1)
                sink_key = (x, y + 1, ptc_y2) # Target CHANY is at y + 1 (ABOVE)
                
                if src_key in chany_dict and sink_key in chany_dict:
                    src_id = chany_dict[src_key]
                    sink_id = chany_dict[sink_key]
                    
                    new_edge_forward = ET.Element('edge')
                    new_edge_forward.set('src_node', src_id)
                    new_edge_forward.set('sink_node', sink_id)
                    new_edge_forward.set('switch_id', '2')
                    
                    new_edge_backward = ET.Element('edge')
                    new_edge_backward.set('src_node', sink_id)
                    new_edge_backward.set('sink_node', src_id)
                    new_edge_backward.set('switch_id', '2')
                    
                    rr_edges.append(new_edge_forward)
                    rr_edges.append(new_edge_backward)
                    edges_added_count_chany_above += 2

print(f"  -> Pass 4 complete: {edges_added_count_chany_above} edges added.")

# Step 7: Add new one-to-one bidirectional edges (CHANY 0-7 to CHANY 8-15 SAME LEVEL)
print("Pass 5: Adding new edges (CHANY 0-7 to CHANY 8-15 SAME LEVEL)...")
edges_added_count_chany_same_level = 0

if rr_edges is not None:
    for x in range(0, 11):          
        for y in range(0, 11):      
            for ptc_y1 in range(0, 8):  
                
                ptc_y2 = ptc_y1 + 8
                src_key = (x, y, ptc_y1)
                sink_key = (x, y, ptc_y2) # Target CHANY is at the same y level
                
                if src_key in chany_dict and sink_key in chany_dict:
                    src_id = chany_dict[src_key]
                    sink_id = chany_dict[sink_key]
                    
                    new_edge_forward = ET.Element('edge')
                    new_edge_forward.set('src_node', src_id)
                    new_edge_forward.set('sink_node', sink_id)
                    new_edge_forward.set('switch_id', '2')
                    
                    new_edge_backward = ET.Element('edge')
                    new_edge_backward.set('src_node', sink_id)
                    new_edge_backward.set('sink_node', src_id)
                    new_edge_backward.set('switch_id', '2')
                    
                    rr_edges.append(new_edge_forward)
                    rr_edges.append(new_edge_backward)
                    edges_added_count_chany_same_level += 2

print(f"  -> Pass 5 complete: {edges_added_count_chany_same_level} edges added.")

# Step 8: Add new one-to-one bidirectional edges (CHANY 0-7 to CHANX 0-7 RIGHT)
print("Pass 6: Adding new edges (CHANY 0-7 to CHANX 0-7 RIGHT)...")
edges_added_count_chany_chanx_right = 0

if rr_edges is not None:
    for x in range(0, 11):          
        for y in range(0, 11):      
            for ptc in range(0, 8):  
                
                src_key = (x, y, ptc)
                sink_key = (x + 1, y, ptc) # Target CHANX is immediately to the RIGHT
                
                if src_key in chany_dict and sink_key in chanx_dict:
                    src_id = chany_dict[src_key]
                    sink_id = chanx_dict[sink_key]
                    
                    new_edge_forward = ET.Element('edge')
                    new_edge_forward.set('src_node', src_id)
                    new_edge_forward.set('sink_node', sink_id)
                    new_edge_forward.set('switch_id', '0')
                    
                    new_edge_backward = ET.Element('edge')
                    new_edge_backward.set('src_node', sink_id)
                    new_edge_backward.set('sink_node', src_id)
                    new_edge_backward.set('switch_id', '0')
                    
                    rr_edges.append(new_edge_forward)
                    rr_edges.append(new_edge_backward)
                    edges_added_count_chany_chanx_right += 2

print(f"  -> Pass 6 complete: {edges_added_count_chany_chanx_right} edges added.")

# Step 9: Add new one-to-one bidirectional edges (CHANY 8-15 to CHANY 8-15 ABOVE)
print("Pass 7: Adding new edges (CHANY 8-15 to CHANY 8-15 ABOVE)...")
edges_added_count_chany_above_8_15 = 0

if rr_edges is not None:
    for x in range(0, 11):          
        for y in range(0, 11):      
            for ptc in range(8, 16):  
                
                src_key = (x, y, ptc)
                sink_key = (x, y + 1, ptc) # Target CHANY is at y + 1 (ABOVE)
                
                if src_key in chany_dict and sink_key in chany_dict:
                    src_id = chany_dict[src_key]
                    sink_id = chany_dict[sink_key]
                    
                    new_edge_forward = ET.Element('edge')
                    new_edge_forward.set('src_node', src_id)
                    new_edge_forward.set('sink_node', sink_id)
                    new_edge_forward.set('switch_id', '2')
                    
                    new_edge_backward = ET.Element('edge')
                    new_edge_backward.set('src_node', sink_id)
                    new_edge_backward.set('sink_node', src_id)
                    new_edge_backward.set('switch_id', '2')
                    
                    rr_edges.append(new_edge_forward)
                    rr_edges.append(new_edge_backward)
                    edges_added_count_chany_above_8_15 += 2

print(f"  -> Pass 7 complete: {edges_added_count_chany_above_8_15} edges added.")

# Step 10: Write the modified tree to the output file
total_new_edges = (edges_added_count_above + 
                   edges_added_count_same_level_8_15 + 
                   edges_added_count_same_level_0_7 +
                   edges_added_count_chany_above +
                   edges_added_count_chany_same_level +
                   edges_added_count_chany_chanx_right +
                   edges_added_count_chany_above_8_15)

print(f"Total new bidirectional edges added across all passes: {total_new_edges}.")
print(f"Saving the modified graph to: {output_xml_path}...")

# Write back the XML while maintaining the XML declaration
tree.write(output_xml_path, encoding='utf-8', xml_declaration=True)
print("Process completed successfully.")
