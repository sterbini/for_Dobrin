# %% using /mnt/hdd1/sterbini/for_Dobrin/miniforge
1+1
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

# Get twiss data to extract s-positions
twiss = lhcb1.twiss4d()

for elem_name in bbcw_elements:
    element = lhcb1[elem_name]

    # Get s-position
    elem_index = lhcb1.element_names.index(elem_name)
    s_pos = twiss.s[elem_index]

    print("=" * 70)
    print(f"Element: {elem_name}")
    print(f"S-position: {s_pos:.6f} m")
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

lhcb1.ref['i_wire.a.4l1.b1'].xdeps.info(limit=None)

lhcb1.element_refs['bbcw.a.4l1.b1'].post_subtract_py.xdeps.info(limit=None)

lhcb1.ref['ksl_0_wire.a.4l1.b1'].xdeps.info(limit=None)
# %%
lhcb1.ref['i_wire.a.4l1.b1'] = 0


for current in ['i_wire.a.4l1.b1','i_wire.a.4l5.b1','i_wire.b.4l1.b1','i_wire.b.4l5.b1']:
    print(f"Current {current}: {lhcb1.ref[current].xdeps.value} A") 
    
print(80 *"=")

tw_zero_current  = lhcb1.twiss4d()

lhcb1.ref['i_wire.a.4l1.b1'] = 350
for current in ['i_wire.a.4l1.b1','i_wire.a.4l5.b1','i_wire.b.4l1.b1','i_wire.b.4l5.b1']:
    print(f"Current {current}: {lhcb1.ref[current].xdeps.value} A") 

tw_100_current  = lhcb1.twiss4d()

    
# %%
from matplotlib import pyplot as plt
plt.figure(figsize=(10, 6))
plt.plot(tw_zero_current.s,  tw_zero_current.x- tw_100_current.x, label='x (0 A)', color='blue')
plt.plot(tw_zero_current.s, tw_zero_current.y- tw_100_current.y, label='y (0 A)', color='red')
plt.xlabel('s [m]')
plt.ylabel('Delta [m]')
plt.legend()
plt.show()

# %%
