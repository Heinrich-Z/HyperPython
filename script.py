import hm
import hm.entities as ent

# open an empty
model = hm.Model()

def beam_section(**kwargs):
    # T stringer cross-section
    beamsection = ent.Beamsection(model, 1)  # T section
    beamsection.beamsect_dim2 = kwargs['T']['DIM2']
    beamsection.beamsect_dim4 = kwargs['T']['DIM4']
    # compute centroid offset
    z_ec = beamsection.results_centroid0
    offset = beamsection.beamsect_dim2 / 2 - z_ec
    # update offset
    properties_collection = hm.Collection(model, hm.FilterByEnumeration(ent.Property, ids=[12]))
    elements_collection = hm.Collection(model, hm.FilterByCollection(ent.Element, ent.Property), properties_collection)
    elements_collection.set_values('OS_ELEMS_LOCAL_OFFSETA', [0, 0, -offset])
    elements_collection.set_values('OS_ELEMS_LOCAL_OFFSETB', [0, 0, -offset])

    # Omega stringer cross-section
    beamsection = ent.Beamsection(model, 3)
    beamsection.beamsect_dim1 = kwargs['Omega']['DIM1']
    beamsection.beamsect_dim2 = kwargs['Omega']['DIM2']
    # compute centroid offset
    # note the offset is calculated differently for the Omega stringer
    z_ec = beamsection.results_centroid0
    offset = beamsection.beamsect_dim1 / 2 + z_ec

    # update offset
    properties_collection = hm.Collection(model, hm.FilterByEnumeration(ent.Property, ids=[13]))
    elements_collection = hm.Collection(model, hm.FilterByCollection(ent.Element, ent.Property), properties_collection)
    elements_collection.set_values('OS_ELEMS_LOCAL_OFFSETA', [0, 0, -offset])
    elements_collection.set_values('OS_ELEMS_LOCAL_OFFSETB', [0, 0, -offset])


def skin_panel(panel_array):
    for i, t in enumerate(panel_array):
        print(f"Processing panel number {i + 1}...")
        prop = ent.Property(model, i + 1)
        prop.PSHELL_T = t
        print(f"Setting elastic center of panel number {i + 1}")
        properties_collection = hm.Collection(model, hm.FilterByEnumeration(ent.Property, ids=[prop.id]))
        elements_collection = hm.Collection(model, hm.FilterByCollection(ent.Element, ent.Property),
                                            properties_collection)
        elements_collection.set_values('ZOFFS', round(t / 2, 2))


def mass_calculation():
    comp_collection = hm.Collection(model, ent.Component, list(range(1, 20)))
    _, result = model.hm_getmass(collection=comp_collection, mass_type=0)
    mass = result.totalmass * 1000
    print("MASS (kg): ", mass)
    return


def main():
    # define panel thickness
    panel_param = [4.9, 4.9, 4.9, 4.9, 4.9, 4.9, 4.9, 4.9, 4.9, 4.9]
    # define stringer parameter
    stringer_param = {"T": {"DIM2": 51.5, "DIM4": 1.5}, "Omega": {"DIM1": 31, "DIM2": 2.0}}
    skin_panel(panel_param)
    beam_section(**stringer_param)
    mass_calculation()


if __name__ == "__main__":
    main()
