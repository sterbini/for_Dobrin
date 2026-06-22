# %% using /mnt/hdd1/sterbini/for_Dobrin/miniforge
1+1
# %% Import json file
 
import xtrack as xt
collider = xt.Multiline.from_json('/home/kaltchev/collider_wires.json')
lhcb1 = collider.lines['lhcb1']

# %% Inspection of the wires

# Extract all wire element names in lhcb1
wire_elements = [name for name in lhcb1.element_names if 'bbcw' in name]

print(f"Total wire elements in lhcb1: {len(wire_elements)}\n")
print("Wire elements:")
for wire in sorted(wire_elements):
    print(f"  {wire}")

# %%

bbcw_elements = ['bbcw.a.4l1.b1', 'bbcw.b.4l1.b1', 'bbcw.a.4l5.b1', 'bbcw.b.4l5.b1']

# Get twiss data to extract s-positions
twiss = lhcb1.twiss4d()

for elem_name in bbcw_elements:
    element = lhcb1[elem_name]

    # Get s-position
    elem_index = lhcb1.element_names.index(elem_name)
    s_pos = twiss.s[elem_index]
    x_co = twiss.x[elem_index]
    y_co = twiss.y[elem_index]
    print("=" * 70)
    print(f"Element: {elem_name}")
    print(f"s-position: {s_pos:.6f} m")
    print(f"x-coordinate co: {x_co:.6f} m")
    print(f"y-coordinate co: {y_co:.6f} m")
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

lhcb1.ref['knl_0_wire.a.4l1.b1'].xdeps.info(limit=None)

# %%
# d_wire.a.4l1.b1
lhcb1['d_wire.a.4l1.b1']
# %%
# co_x_wire.a.4l1.b1
lhcb1['co_x_wire.a.4l1.b1']

# %%

lhcb1['on_x1'] = 0

lhcb1.ref['i_wire.a.4l1.b1'] = 0
lhcb1.ref['i_wire.b.4l1.b1'] = 0


def print_wire_currents(lhcb1, wire_names):
    print(80 *"=")
    for current in wire_names:
        print(f"Current {current}: {lhcb1.ref[current].xdeps.value} A") 
    print(80 *"=")
   
print_wire_currents(lhcb1, ['i_wire.a.4l1.b1','i_wire.b.4l1.b1','i_wire.a.4l5.b1','i_wire.b.4l5.b1'])

tw_zero_current  = lhcb1.twiss4d()

lhcb1.ref['i_wire.a.4l1.b1'] = 100
lhcb1.ref['i_wire.b.4l1.b1'] = 100

print(lhcb1.element_refs['bbcw.a.4l1.b1'].post_subtract_py.xdeps.value)
print(lhcb1.element_refs['bbcw.b.4l1.b1'].post_subtract_py.xdeps.value)

print_wire_currents(lhcb1, ['i_wire.a.4l1.b1','i_wire.b.4l1.b1','i_wire.a.4l5.b1','i_wire.b.4l5.b1'])


tw_100_current  = lhcb1.twiss4d()

    
# %%
from matplotlib import pyplot as plt
plt.figure(figsize=(10, 6))
plt.plot(tw_zero_current.s, tw_zero_current.x - tw_100_current.x, label='DeltaX (0-100 A)', color='blue')
plt.plot(tw_zero_current.s, tw_zero_current.y - tw_100_current.y, label='DeltaY (0-100 A)', color='red')
plt.xlabel('s [m]')
plt.ylabel('Delta [m]')
plt.legend()
plt.show()

# %%
