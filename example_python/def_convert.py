
proj_name = "CHIP_DataConverter"
pwd = f"./ashes/{proj_name}"
#input_file_path = f"{pwd}/islands_exp_350nm_qroute.def"
#output_file_path = f"{pwd}/islands_exp_350nm_blockages.def"

pwd = "."

input_file_path = f"{pwd}/{proj_name}_qroute.def"
output_file_path = f"{pwd}/{proj_name}_blockages.def"

def convert_blockages(content):
    # Split the content by lines
    lines = content.splitlines()
    
    # To store the converted content
    converted_lines = []
    
    # Variables to manage state
    inside_blockages = False
    current_layer = []
    current_rects = []
    logged_end_nets = False
    
    for line in lines:
        stripped_line = line.strip()
        
        if stripped_line.startswith("BLOCKAGES"):
            inside_blockages = True
            converted_lines.append(line)
            continue
        
        if inside_blockages:
            if stripped_line.startswith("END BLOCKAGES"):
                # We've reached the end of the blockages section, convert all collected rects
                for ind, rect in enumerate(current_rects):
                    converted_lines.append(f"  - LAYER {current_layer[ind]}")
                    converted_lines.append(f"    {rect}")
                converted_lines.append("END BLOCKAGES")
                
                # Reset the state variables
                inside_blockages = False
                current_layer = ""
                current_rects = []
                continue
            
            if stripped_line.startswith("-"):
                # Extract the layer name correctly
                current_layer.append(stripped_line.split()[1])
                continue
            
            if stripped_line.startswith("POLYGON") or stripped_line.startswith("RECT"):
                # Collect rect definitions
                current_rects.append(stripped_line)
                continue
            
            if stripped_line == "END":
                # Skip this line as we handle ending the block later
                continue
        else:
            converted_lines.append(line)
    
    # Join the converted lines back into a single string
    return "\n".join(converted_lines)

# Convert the content again with the updated function
with open(input_file_path, 'r') as file:
    before_content = file.read()

converted_content = convert_blockages(before_content)

# Save the corrected converted content to the new output file
with open(output_file_path, 'w') as file:
    file.write(converted_content)

output_file_path

print("Converted DEF")
