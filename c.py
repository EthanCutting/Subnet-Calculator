import tkinter as tk
import ipaddress
def calculate_subnet(ip_address, subnet_mask):
    ip_bin = ''.join(format(int(octet), '08b') for octet in ip_address.split('.'))
    mask_bin = ''.join(format(int(octet), '08b') for octet in subnet_mask.split('.'))
    network_id_bin = ''.join(str(int(ip_bit) & int(mask_bit)) for ip_bit, mask_bit in zip(ip_bin, mask_bin))

    # Calculate number of available hosts in the subnet
    num_hosts = 2 ** (32 - sum(int(bit) for bit in mask_bin))

    # Calculate usable IP range
    usable_range_start = network_id_bin[:-1] + '1'  # Increment the last host bit for the first usable IP
    usable_range_end = bin(int(network_id_bin, 2) + num_hosts - 2)[2:].zfill(32)  # Calculate last usable IP

    network_id = '.'.join(str(int(network_id_bin[i:i + 8], 2)) for i in range(0, 32, 8))
    usable_range = '.'.join(str(int(usable_range_start[i:i + 8], 2)) for i in range(0, 32, 8)) + " - " + \
                   '.'.join(str(int(usable_range_end[i:i + 8], 2)) for i in range(0, 32, 8))
    
    # Calculate broadcast address by applying bitwise OR operation with inverted subnet mask
    inverted_mask_bin = ''.join(str(1 - int(mask_bit)) for mask_bit in mask_bin)
    broadcast_address_bin = ''.join(str(int(ip_bit) | int(inverted_mask_bit)) for ip_bit, inverted_mask_bit in zip(network_id_bin, inverted_mask_bin))
    broadcast_address = '.'.join(str(int(broadcast_address_bin[i:i + 8], 2)) for i in range(0, 32, 8))

    return {
        "Network ID": network_id,
        "Usable Range": usable_range,
        "Subnet Mask": subnet_mask,
        "Broadcast Address": broadcast_address
    }


# Define the is_valid_ip and is_valid_subnet functions
def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def is_valid_subnet(subnet):
    try:
        ipaddress.ip_network(subnet, strict=False)
        return True
    except ValueError:
        return False

# Define the show_subnet_details function
def show_subnet_details():
    ip_address = ip_entry.get()
    subnet_mask = mask_entry.get()
    
    print("IP Address:", ip_address)
    print("Subnet Mask:", subnet_mask)

    if not is_valid_ip(ip_address):
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Invalid IP Address")
        return

    if not is_valid_subnet(subnet_mask):
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Invalid Subnet Mask")
        return

    subnet_details = calculate_subnet(ip_address, subnet_mask)
    
    print("Subnet Details:", subnet_details)  # Print subnet details for debugging
    
    result_text.delete(1.0, tk.END)
    for key, value in subnet_details.items():
        result_text.insert(tk.END, f"{key}: {value}\n")

# Create the root window
root = tk.Tk()
root.title("Subnet Calculator")

# Create IP Address label and entry
ip_label = tk.Label(root, text="IP Address:")
ip_label.pack()
ip_entry = tk.Entry(root)
ip_entry.pack()
ip_entry.configure(bg="light gray")
ip_entry.pack()

# Create Subnet Mask label and entry
mask_label = tk.Label(root, text="Subnet Mask:")
mask_label.pack()
mask_entry = tk.Entry(root)
mask_entry.pack()
mask_entry.configure(bg="light gray")

mask_entry.pack()

# Create Calculate button
calculate_button = tk.Button(root, text="Calculate", command=show_subnet_details)
calculate_button.pack()

# Create Result Text area
result_text = tk.Text(root)
root.configure(bg="light blue")  
result_text.pack()
result = tk.Entry(root)
result_text.pack()
result_text.configure(bg="light gray")


# Start the main event loop
root.mainloop()
