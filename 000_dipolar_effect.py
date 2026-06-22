# %% using /mnt/hdd1/sterbini/for_Dobrin/miniforge



# %% Import json file
 
import xtrack as xt
collider = xt.Multiline.from_json('/home/kaltchev/collider_wires.json')
lhcb1 = collider.lines['lhcb1']


# %% Twiss 4D 

lhcb1.twiss4d()

# %% Inspection of the wires

# Extract all wire element names in lhcb1
wire_elements = [name for name in lhcb1.element_names if 'bbcw' in name]

print(f"Total wire elements in lhcb1: {len(wire_elements)}\n")
print("Wire elements:")
for wire in sorted(wire_elements):
    print(f"  {wire}")

# %%

bbcw_elements = ['bbcw.a.4l1.b1', 'bbcw.a.4l5.b1', 'bbcw.b.4l1.b1', 'bbcw.b.4l5.b1']

for elem_name in bbcw_elements:
    element = lhcb1[elem_name]

    print("=" * 70)
    print(f"Element: {elem_name}")
    print("=" * 70)
    print(f"Type: {type(element).__name__}\n")

    print("Attributes:")
    print("-" * 70)
    for attr in sorted(dir(element)):
        if not attr.startswith('_'):
            try:
                value = getattr(element, attr)
                if not callable(value):
                    print(f"  {attr:30s} = {value}")
            except:
                pass

    print("\n" + "Key Properties:")
    print("-" * 70)
    if hasattr(element, '__dict__'):
        for key, val in sorted(element.__dict__.items()):
            if not key.startswith('_'):
                print(f"  {key:30s} = {val}")

    print("\n")
# %%
