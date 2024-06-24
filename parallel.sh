#!/bin/bash

# Ensure a default directory is provided
export find_dir="data/seantest/not_reconstructing_smiles"
export output_dir="out/not_reconstructing_smiles"

if [ -n "$1" ]; then
    export find_dir="$1"
fi

if [ -n "$2" ]; then
    export output_dir="$2"
fi

# Ensure the output directory does not exist
if [ -d "${output_dir}" ]; then
    echo "${output_dir} already exists. Do you want to "
    read -p "(r)ename it, (d)elete it, (i)gnore it or (c)ancel? (r/d/i/c): " choice
    case "$choice" in
        r|R)
            read -p "Enter new name: " new_name
            mv "${output_dir}" "${new_name}"
            ;;
        d|D)
            rm -r "${output_dir}"
            ;;
        i|I)
            echo "Continuing with existing directory."
            ;;
        c|C)
            echo "Script cancelled by user."
            exit 0
            ;;
        *)
            echo "Invalid option. Exiting."
            exit 1
            ;;
    esac
fi

# Function to run eMolFrag2 on a file
run_emolfrag() {
    file="$1"
    mkdir -p "${output_dir}"
    input_smi=$(basename "$file" )
    # echo "input_smi: $input_smi"
    input_smi_id="${input_smi%.*}"
    # echo "input_smi_id: $input_smi_id"
    output_path="${output_dir}/${input_smi_id}"
    # echo "output_path: $output_path"
    
    echo "Processing $file... (to ${output_path}/)"
    emolfrag -i "$file" -o "${output_path}" -and 2>&1 | tee "${output_path}_log.txt"
    echo "log file at ${output_path}_log.txt"

    # Move the log file to the output directory
    # mv "${output_path}_log.txt" "${output_path}/${input_smi_id}_log.txt"
}

export -f run_emolfrag

# Find all files in the BrokeFiles directory and pass each one to run_emolfrag using parallel
find $find_dir -type f -name "*.smi" | parallel --bar run_emolfrag
# parallel --bar run_emolfrag :::: failed.txt


echo "All processing done."
