# created by Tianao Henry Zhang
# do not distribute without the creator's consent
# this script can only run in HyperMesh Python interpreter
# version 1.0
import hm
import hw
import hw.hv as hv
import hm.entities as ent
from datetime import datetime
import os
import csv

MODEL_FILE = r"C:\Users\henry\Desktop\ASE\Project\Assignment 2\ASE_Project_Part2_3800178\leo_redesign_model.fem"
RESULT_FILE = r"C:\Users\henry\Desktop\ASE\Project\Assignment 2\ASE_Project_Part2_3800178\leo_redesign_model.h3d"
OUTPUT_DIR = r"C:\Users\henry\Desktop\ASE\Project\Assignment 2\ASE_Project_Part2_3800178\metallic\leo_redesign"
LOADCASES = [1, 2]


def result_query(**kwargs):

    # create and reset HyperView session
    ses = hw.Session()
    ses.new()
    win = ses.get(hw.Window)
    win.type = 'animation'
    hw.evalHWC("result scalar legend values format=fixed precision=12")

    # loading the model and result
    win.addModelAndResult(model=MODEL_FILE, result=RESULT_FILE)
    print("Model and results loaded.")
    result = ses.get(hv.Result)

    # result querying
    # set the numeric precision to 12
    legend = hv.LegendScalar(numericPrecision=12)

    query_tool = hv.QueryResultsTool()
    # all elements
    element_collection = hv.Collection(hv.Element)
    query_tool.collection = element_collection
    # NOTE: This line is validated in HyperView console
    query_tool.setDataSourceQuery([['element', 'id'], ['element', 'config'], ['contour', 'value']])

    # key = {loadcase_id, element_id}, value = dict
    data_type = kwargs["data_type"]
    comp_list = kwargs["data_component"]

    # for 2D elements: id, lc, XX, XY, YY, vonMises
    final_table = []

    for lc in LOADCASES:
        lc_result_table = {}
        # iterate through load case
        print(f"Processing load case: {lc}...")

        result.subcase = lc
        simulation_id = result.getSimulationIds(lc)
        result.simulation = simulation_id[0]

        # resolve datatype name from actual result file
        print(f"Selecting data type: {data_type}")

        for comp in comp_list:
            # iterate through data components
            if data_type == "Element Stresses (2D & 3D)":
                # result definition for 2D and 3D elements
                res_scalar = hv.ResultDefinitionScalar(
                    dataType=data_type,
                    dataComponent=comp,
                    layer="Mid",
                    system=1  # in hv this should be an integer
                )

                result.plot(res_scalar)
                data = query_tool.query()
                for row in data:
                    if row[1] == '104':
                        if row[0] not in lc_result_table:
                            lc_result_table[row[0]] = {comp: row[2]}
                        else:
                            lc_result_table[row[0]][comp] = row[2]
                    else:
                        continue

            elif data_type == "Element Stresses (1D)":
                # result definition for 1D elements
                res_scalar = hv.ResultDefinitionScalar(
                    dataType=data_type,
                    dataComponent=comp,
                )

                result.plot(res_scalar)
                data = query_tool.query()
                for row in data:
                    if row[1] == '60':
                        if row[0] not in lc_result_table:
                            lc_result_table[row[0]] = {comp: row[2]}
                        else:
                            lc_result_table[row[0]][comp] = row[2]
                    else:
                        continue

            else:
                print("Data type does not exist")
                return

        lc_result_list = [{**{"Elements": eid, "LC": lc}, **contour} for eid, contour in lc_result_table.items()]
        final_table += lc_result_list

    return final_table


def main():
    # generate timestamp for the output csv file name
    timestamp = datetime.now().strftime("%m%d%H%M")

    # generate stress report for 2D shell elements
    shell_property = {"data_type": "Element Stresses (2D & 3D)", "data_component": ['XX', 'XY', 'YY', 'vonMises']}
    stress_report_2d = result_query(**shell_property)
    # save to csv file
    csv_filename = f"stress_report_2d.csv"
    output_path = os.path.join(OUTPUT_DIR, csv_filename)
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=stress_report_2d[0].keys())
        writer.writeheader()
        writer.writerows(stress_report_2d)
    print(f"Saving 2D elements stress report to {output_path}")

    # generate stress report for 1D bar elements
    bar_property = {"data_type": "Element Stresses (1D)", "data_component": ['CBAR/CBEAM Axial Stress']}
    stress_report_1d = result_query(**bar_property)
    # save to csv file
    csv_filename = f"stress_report_1d.csv"
    output_path = os.path.join(OUTPUT_DIR, csv_filename)
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=stress_report_1d[0].keys())
        writer.writeheader()
        writer.writerows(stress_report_1d)
    print(f"Saving 1D elements stress report to {output_path}")


if __name__ == '__main__':
    main()

