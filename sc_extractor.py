#!/usr/bin/env python3
import sc_compression
import os
import argparse

def decompress_file(input_path, output_path):
    try:
        with open(input_path, 'rb') as f:
            data = f.read()
            result = sc_compression.decompress(data)
            decompressed = result[0] if isinstance(result, tuple) else result
            with open(output_path, 'wb') as out:
                out.write(decompressed)
            print(f"OK: {input_path} -> {output_path}")
            return True
    except Exception as e:
        print(f"FAIL: {input_path} - {e}")
        return False

def process(input_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if os.path.isdir(input_path):
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.endswith('.sc') or file.endswith('.csv'):
                    in_file = os.path.join(root, file)
                    rel_path = os.path.relpath(in_file, input_path)
                    out_file = os.path.join(output_dir, rel_path + '.decrypted')
                    out_dir = os.path.dirname(out_file)
                    if not os.path.exists(out_dir):
                        os.makedirs(out_dir)
                    decompress_file(in_file, out_file)
    else:
        base = os.path.basename(input_path)
        out_file = os.path.join(output_dir, base + '.decrypted')
        decompress_file(input_path, out_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="SC-Extractor")
    parser.add_argument('-i', '--input', required=True, help='Input file or folder')
    parser.add_argument('-o', '--output', required=True, help='Output folder')
    args = parser.parse_args()
    process(args.input, args.output)
