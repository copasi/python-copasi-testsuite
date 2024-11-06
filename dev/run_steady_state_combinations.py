import sys
import os
import logging
import argparse
import datetime

import basico
import basico.processing as processing

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(_THIS_DIR, '..'))

from copasi_test.ReportParserSteadyState import ReportParserSteadyState

logger = logging.getLogger(__name__)

CRITERIA = ["Distance", "Rate", "Distance And Rate"]


def _get_method(newton, forward):
    if newton and forward:
        return "both"
    if newton:
        return "newton"
    if forward:
        return "forward"

    return "none"

def get_text_for_result(resultCode):
    """
       - `-1`: error
       - `0`: not found
       - `1`: steady state found
       - `2`: equillibrium steady state found
       - `3`: steady state with negative concentrations found
    """
    if resultCode == -1:
        return "error"
    if resultCode == 0:
        return "not found"
    if resultCode == 1:
        return "steady state found"
    if resultCode == 2:
        return "equillibrium steady state found"
    if resultCode == 3:
        return "steady state with negative concentrations found"

    return "error"

def get_symbol_for_result(resultCode):
    """
       - `-1`: error
       - `0`: not found
       - `1`: steady state found
       - `2`: equillibrium steady state found
       - `3`: steady state with negative concentrations found
    """
    if resultCode == -1:
        return "X"
    if resultCode == 0:
        return "N"
    if resultCode == 1:
        return "S"
    if resultCode == 2:
        return "Eq"
    if resultCode == 3:
        return "Neg"

    return "X"

def get_symbol_for_report_status(status):
    """
    - `A steady state with given resolution was found.`: S
    - `No steady state with given resolution was found!`: N
    - `An equilibrium steady state (zero fluxes) was found.`: Eq
    - `An invalid steady state (negative concentrations) was found.`: Neg
    - `Invalid steady state report`: X
    """
    if status == "A steady state with given resolution was found.":
        return "S"
    if status == "No steady state with given resolution was found!":
        return "N"
    if status == "An equilibrium steady state (zero fluxes) was found.":
        return "Eq"
    if status == "An invalid steady state (negative concentrations) was found.":
        return "Neg"
    if status == "Invalid steady state report":
        return "X"

    return "X"

def run_steady_state_for_file(file_name, copasi_se=None, output_dir='./out/'):
    logger.info("Running steady state for file: %s" % file_name)

    # if output directory does not exist, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    result_dict = {
        'filename': os.path.basename(file_name),
    }

    dm = basico.load_model(file_name)

    # run the steady state for the different combinations
    for criterion in CRITERIA:
        criterion_dict = {}
        for newton in [True, False]:
            for forward in [True, False]:
                if not newton and not forward:
                    continue
                
                settings = basico.get_task_settings("Steady-State")
                settings['method']['Use Integration'] = forward
                settings['method']['Use Newton'] = newton
                settings['method']['Use Back Integration'] = False
                settings['method']['Target Criterion'] = criterion
                settings['method']['Maximum duration for forward integration'] = 10000000000.0

                settings['report']['filename'] = "%s_%s_%s_%s.txt" % (os.path.basename(file_name), criterion, forward, newton)
                settings['report']['append'] = False
                settings['report']['confirm_overwrite'] = False

                basico.set_task_settings("Steady-State", settings)

                # set the output cps file in the output dir, with the criterion, newton and forward flags in the name
                cps_file = os.path.join(output_dir, "%s_%s_%s_%s.cps" % (os.path.basename(file_name), criterion, forward, newton))
                basico.save_model(cps_file, model=dm)
                


                result = -1
                try:
                    result = basico.run_steadystate(model=dm)
                except:
                    pass

                logger.info("Steady state for file %s with criterion %s, newton %s, forward %s: %s" % (file_name, criterion, newton, forward, get_text_for_result(result)))

                method = _get_method(newton, forward)

                criterion_dict[method] = {
                    'symbol':  get_symbol_for_result(result), 
                    'cps_file': cps_file, 
                    'report_file': os.path.join(output_dir, settings['report']['filename']),
                    'tooltip': get_text_for_result(result),
                    'result': result
                }
                
        result_dict[criterion] = criterion_dict
                
    basico.remove_datamodel(dm)
    basico.remove_user_defined_functions()

    print(result_dict)
    return result_dict

def generate_files(file_name, output_dir='./out/'):
    
    # if output directory does not exist, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    cps_files = []

    dm = basico.load_model(file_name)

    # run the steady state for the different combinations
    for criterion in CRITERIA:
        for newton in [True, False]:
            for forward in [True, False]:
                if not newton and not forward:
                    continue
                
                settings = basico.get_task_settings("Steady-State")
                settings['method']['Use Integration'] = forward
                settings['method']['Use Newton'] = newton
                settings['method']['Use Back Integration'] = False
                settings['method']['Target Criterion'] = criterion
                settings['method']['Maximum duration for forward integration'] = 10000000000.0

                settings['report']['filename'] = "%s_%s_%s_%s.txt" % (os.path.basename(file_name), criterion, forward, newton)
                settings['report']['append'] = False
                settings['report']['confirm_overwrite'] = False

                settings['scheduled'] = True

                basico.set_task_settings("Steady-State", settings)

                # set the output cps file in the output dir, with the criterion, newton and forward flags in the name
                cps_file = os.path.join(output_dir, "%s_%s_%s_%s.cps" % (os.path.basename(file_name), criterion, forward, newton))
                basico.save_model(cps_file, model=dm)
                cps_files.append(os.path.abspath(cps_file))
                                
    basico.remove_datamodel(dm)
    basico.remove_user_defined_functions()

    return cps_files



def run_steady_state_combinations(file_names, output_dir='./out/'):

    results = []

    for file_name in file_names:
        try:
            result_dict = run_steady_state_for_file(file_name)
            results.append(result_dict)
        except:
            pass
    
    generate_result_table(results, output_dir)


def run_steady_state_combinations_with_copasi_se(file_names, copasi_se, output_dir='./out/', max_time=20):

    # generate all files 
    copasi_files_to_run = []
    for file_name in file_names:
        try:
            copasi_files_to_run += generate_files(file_name, output_dir)
        except:
            pass

    # run with COPASI SE in parallel
    processing.process_files(copasi_files_to_run, copasi_se=copasi_se, max_time=max_time)

    result_dict = {}

    # read report files and collect results
    for file in copasi_files_to_run:
        # replace trailing .cps with .txt
        
        report_base = file[:-4]
        report_file = report_base + ".txt"
        report_base = os.path.basename(report_base)
        
        # extract the steady state status from the report
        try:
            parser = ReportParserSteadyState()
            parser.parserFile(report_file)
            status = parser.status
        except:
            status = "error"


        # extract filename, criterion, forward and newton from the filename
        # example file names: 
        #
        #   02_scan_ss_cont.cps_Distance And Rate_False_True.cps
        #
        # here filename is 02_scan_ss_cont.cps, criterion is Distance And Rate, forward is False and newton is True
        #
        # so we loop through criteria, and split by them, then split by _ to get forward and newton
        for criteria in CRITERIA: 
            if '_' + criteria + '_' not in report_base:
                continue

            chunks = report_base.split('_' + criteria + '_')
            model_name = chunks[0]

            if model_name not in result_dict:
                result_dict[model_name] = {
                    'filename': model_name                    
                }

            if criteria not in result_dict[model_name]:
                result_dict[model_name][criteria] = {}

            chunks = chunks[1].split('_')
            forward = chunks[0] == 'True'
            newton = chunks[1] == 'True'

            method = _get_method(newton, forward)

            if method not in result_dict[model_name][criteria]:
                result_dict[model_name][criteria][method] = {}

            criterion_dict = result_dict[model_name][criteria]

            criterion_dict[method] = {
                'symbol':  get_symbol_for_report_status(status), 
                'cps_file': os.path.basename(file), 
                'report_file': os.path.basename(report_file),
                'tooltip': status,
            }        
        

    # split the result_dict into a list    
    results = []
    for key in result_dict:
        results.append(result_dict[key])

    generate_result_table(results, output_dir)


def generate_result_table(results, output_dir):
    # generate result table as HTML
    with open(os.path.join(_THIS_DIR, 'steady-state-template.html'), 'r') as file:
        template = file.read()

    # generate the table rows
    rows = ""

    for result in results:
        row = "<tr>"
        row += "<td>%s</td>" % result['filename']
        for criterion in CRITERIA:
            for method in ['forward', 'newton', 'both']:
                if method in result[criterion]:                    
                    rel_path = os.path.basename(result[criterion][method]["cps_file"])
                    rel_path = rel_path.replace("\\", "/")
                    invoke_Javascript = f'javascript:openCopasi("{rel_path}")'
                    row += f"<td><a href='{rel_path}' onclick='{invoke_Javascript}' target='_blank' title='{result[criterion][method]['tooltip']}'  > {result[criterion][method]['symbol']} </a></td>"
                else:
                    row += "<td></td>"
        row += "</tr>"

        rows += row

    # replace the string <!--ROWS--> in the template with the rows
    template = template.replace("<!--ROWS-->", rows)

    # replace the string <!--TIMESTAMP--> in the template with the current timestamp
    template = template.replace("<!--TIMESTAMP-->", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    with open(os.path.join(output_dir, 'steady-state-results.html'), 'w') as file:
        file.write(template)

# use argparse to parse command line arguments, we need one required argument, the 
# path to the file or directory. As optional arguments we can specify the output directory (defaults to ./out/), 
# the maximum time for the run with CopasiSE (defaults to 20 seconds) and the CopasiSE executable (defaults to CopasiSE)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run steady state combinations for COPASI models.')
    parser.add_argument('path', type=str, help='Path to the file or directory containing COPASI models.')
    parser.add_argument('--output_dir', type=str, default='./out/', help='Output directory for results (default ./out/).')
    parser.add_argument('--max_time', type=int, default=20, help='Maximum time for the run with CopasiSE (default 20 seconds).')
    parser.add_argument('--copasi_se', type=str, default='CopasiSE', help='Path to the CopasiSE executable. (default CopasiSE)')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    path = args.path
    file_names = []
    # check wether the path is a directory
    if os.path.isdir(path):
        # get all files in the directory
        files = os.listdir(path)
        for file in files:
            if file.endswith(".xml") or file.endswith(".cps"):
                # add full path to the file to the list
                file_names.append(os.path.join(path, file))

    else:
        file_names.append(path)

    # run_steady_state_combinations(file_names)
    run_steady_state_combinations_with_copasi_se(file_names, args.copasi_se, output_dir=args.output_dir, max_time=args.max_time)