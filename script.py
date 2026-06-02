import hm
import hm.entities as ent

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
    print(z_ec, beamsection.beamsect_dim1, offset)

    # update offset
    properties_collection = hm.Collection(model, hm.FilterByEnumeration(ent.Property, ids=[13]))
    elements_collection = hm.Collection(model, hm.FilterByCollection(ent.Element, ent.Property), properties_collection)
    elements_collection.set_values('OS_ELEMS_LOCAL_OFFSETA', [0, 0, -offset])
    elements_collection.set_values('OS_ELEMS_LOCAL_OFFSETB', [0, 0, -offset])


def skin_panel(panel_array):
    print(f"")
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
    if mass < 19.519543162008166:
        print("MASS REQUIREMENT PASSED")
    else:
        print("MASS REQUIREMENT FAILED")


def main():
    """
    model.retainmarkselections(mode=0)
    model.feoutputmergeincludefiles(code=0)
    model.setsubmodeltype(type="HM_INCLUDEFILES")
    model.setentitytypesupportedbyenggid(string_array=hm.hwStringList([]))

    # [TIP]: Command triggers popup window. Enable 'Ignore popups' to ignore it when running the script.
    model.feoutputwithdata(export_template="C:/Program Files/Altair/2025.1/hwdesktop/templates/feoutput/optistruct/optistruct", filename="C:/Users/henry/Desktop/ASE/Project/HyperPython/model/SuperPanel_ASE_Project_Part2_submitted_start_3800178.fem", reserved1=0, reserved2=0, export_type=2, string_array=["HM_NODEELEMS_SET_COMPRESS_SKIP ", "EXPORT_DMIG_LONGFORMAT ", "HMENGINEERING_XML", "HMSUBSYSTEMCOMMENTS_XML", "HMMATCOMMENTS_XML", "HMBOMCOMMENTS_XML", "INCLUDE_RELATIVE_PATH ", "EXPORT_SOLVER_DECK_XML_1 "])
    """

    # panel_param = [4.9, 4.9, 4.9, 4.9, 4.9, 4.9, 4.9, 4.9, 4.9, 4.9]
    panel_param = [4.9] * 10
    stringer_param = {"T": {"DIM2": 51.5, "DIM4": 1.5}, "Omega": {"DIM1": 31, "DIM2": 2.0}}
    skin_panel(panel_param)
    beam_section(**stringer_param)
    mass_calculation()


if __name__ == "__main__":
    main()
