#!/usr/bin/env python3
"""
Extract key parameters from Gekle & Gordillo (2010) CSV data.
- rb_min: minimum jet base radius for Fr=5.1 and 92
- B(Fr): axial velocity coefficient as function of Fr
- Ac(Fr): contraction amplitude as function of Fr
"""

import csv
import math
import os

# Paths
DATA_DIR = r"C:\Users\30856\Desktop\IYPT2026_RingFountain\data\data of Gordillo2010"
FIG10 = os.path.join(DATA_DIR, "fig10_jet_base_rb_zb_vs_time.csv")
FIG19 = os.path.join(DATA_DIR, "fig19_B_function.csv")
FIG25 = os.path.join(DATA_DIR, "fig25_Ac_function.csv")

def read_csv(filepath, has_header=True):
    """Read CSV file into list of dicts."""
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f) if has_header else csv.reader(f)
        rows = list(reader)
    return rows

def extract_rb_min():
    """Extract minimum jet base radius for Fr=5.1 and 92."""
    rows = read_csv(FIG10)
    # Find minimum rb_up for each Fr
    rb_up_Fr5p1 = []
    rb_up_Fr92 = []
    rb_down_Fr5p1 = []
    rb_down_Fr92 = []
    
    for row in rows:
        # Fr=5.1 columns
        if row.get('rb_up_Fr5p1', '').strip():
            rb_up_Fr5p1.append(float(row['rb_up_Fr5p1']))
        if row.get('rb_down_Fr5p1', '').strip():
            rb_down_Fr5p1.append(float(row['rb_down_Fr5p1']))
        # Fr=92 columns
        if row.get('rb_up_Fr92', '').strip():
            rb_up_Fr92.append(float(row['rb_up_Fr92']))
        if row.get('rb_down_Fr92', '').strip():
            rb_down_Fr92.append(float(row['rb_down_Fr92']))
    
    # Compute minima
    rb_min_up_Fr5p1 = min(rb_up_Fr5p1) if rb_up_Fr5p1 else None
    rb_min_down_Fr5p1 = min(rb_down_Fr5p1) if rb_down_Fr5p1 else None
    rb_min_up_Fr92 = min(rb_up_Fr92) if rb_up_Fr92 else None
    rb_min_down_Fr92 = min(rb_down_Fr92) if rb_down_Fr92 else None
    
    # Overall minima (take smaller of up/down)
    rb_min_Fr5p1 = min(rb_min_up_Fr5p1, rb_min_down_Fr5p1) if rb_min_up_Fr5p1 and rb_min_down_Fr5p1 else rb_min_up_Fr5p1 or rb_min_down_Fr5p1
    rb_min_Fr92 = min(rb_min_up_Fr92, rb_min_down_Fr92) if rb_min_up_Fr92 and rb_min_down_Fr92 else rb_min_up_Fr92 or rb_min_down_Fr92
    
    return {
        'Fr5p1': {
            'rb_min_up': rb_min_up_Fr5p1,
            'rb_min_down': rb_min_down_Fr5p1,
            'rb_min_overall': rb_min_Fr5p1,
        },
        'Fr92': {
            'rb_min_up': rb_min_up_Fr92,
            'rb_min_down': rb_min_down_Fr92,
            'rb_min_overall': rb_min_Fr92,
        }
    }

def extract_B_Fr():
    """Extract B(Fr) table."""
    rows = read_csv(FIG19)
    table = []
    for row in rows:
        log10_Fr = float(row['log10_Fr'])
        Fr = 10**log10_Fr
        B_avg = float(row['B_avg'])
        B_min = float(row['B_min'])
        B_max = float(row['B_max'])
        table.append({
            'log10_Fr': log10_Fr,
            'Fr': Fr,
            'B_avg': B_avg,
            'B_min': B_min,
            'B_max': B_max
        })
    return table

def extract_Ac_Fr():
    """Extract Ac(Fr) table."""
    rows = read_csv(FIG25)
    table = []
    for row in rows:
        log10_Fr = float(row['log10_Fr'])
        Fr = 10**log10_Fr
        Ac = float(row['Ac'])
        table.append({
            'log10_Fr': log10_Fr,
            'Fr': Fr,
            'Ac': Ac
        })
    return table

def main():
    print("=== Gekle & Gordillo (2010) Parameter Extraction ===\n")
    
    # 1. rb_min
    print("1. Minimum jet base radius rb_min:")
    rb_data = extract_rb_min()
    for fr_key, vals in rb_data.items():
        print(f"   {fr_key}:")
        print(f"     rb_min_up = {vals['rb_min_up']:.3f}")
        print(f"     rb_min_down = {vals['rb_min_down']:.3f}")
        print(f"     rb_min_overall = {vals['rb_min_overall']:.3f}")
    print()
    
    # 2. B(Fr)
    print("2. Axial velocity coefficient B(Fr):")
    B_table = extract_B_Fr()
    print("   log10(Fr)   Fr         B_avg   B_min   B_max")
    for entry in B_table:
        print(f"   {entry['log10_Fr']:6.1f}       {entry['Fr']:7.1f}   {entry['B_avg']:5.1f}   {entry['B_min']:5.1f}   {entry['B_max']:5.1f}")
    print()
    
    # 3. Ac(Fr)
    print("3. Contraction amplitude Ac(Fr):")
    Ac_table = extract_Ac_Fr()
    print("   log10(Fr)   Fr         Ac")
    for entry in Ac_table:
        print(f"   {entry['log10_Fr']:6.1f}       {entry['Fr']:7.1f}   {entry['Ac']:5.2f}")
    print()
    
    # Save to CSV for easy use
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--save':
        # Save rb_min summary
        with open('rb_min_summary.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Fr', 'rb_min_up', 'rb_min_down', 'rb_min_overall'])
            writer.writerow(['5.1', 
                            rb_data['Fr5p1']['rb_min_up'], 
                            rb_data['Fr5p1']['rb_min_down'], 
                            rb_data['Fr5p1']['rb_min_overall']])
            writer.writerow(['92', 
                            rb_data['Fr92']['rb_min_up'], 
                            rb_data['Fr92']['rb_min_down'], 
                            rb_data['Fr92']['rb_min_overall']])
        print("Saved rb_min_summary.csv")
        
        # Save B(Fr) table
        with open('B_Fr_table.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['log10_Fr', 'Fr', 'B_avg', 'B_min', 'B_max'])
            for entry in B_table:
                writer.writerow([entry['log10_Fr'], entry['Fr'], entry['B_avg'], entry['B_min'], entry['B_max']])
        print("Saved B_Fr_table.csv")
        
        # Save Ac(Fr) table
        with open('Ac_Fr_table.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['log10_Fr', 'Fr', 'Ac'])
            for entry in Ac_table:
                writer.writerow([entry['log10_Fr'], entry['Fr'], entry['Ac']])
        print("Saved Ac_Fr_table.csv")
        print("\nAll tables saved in current directory.")

if __name__ == '__main__':
    main()