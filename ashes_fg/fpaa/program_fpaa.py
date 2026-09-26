import os, sys, subprocess

RASPPATH = os.getenv("RASPPATH", "/home/ubuntu/rasp30")
OFF = "0.000000000000000\n"

## All the command execution code is of the same form
def exec_command(cmd, filename):
    while True:
        try:
            proc = subprocess.run([f"sudo tclsh {RASPPATH}/prog_assembly/libs/tcl/{cmd} {filename}"], shell=True, capture_output=True, text=True)
            output = proc.stdout
            print(output)
            success_message = "Program completed."
            if success_message in output and proc.returncode == 0:
                print("Ran subprocess: success")
                break
            else:
                print(proc.stderr)
                raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
        except subprocess.CalledProcessError:
            print("failed: trying again")

def program(filename):
    exec_command('program.tcl -speed 115200', filename)

def write_mem2_NoRelease(addr, fname):
    exec_command(f'write_mem2_NoRelease.tcl -start_address {addr} -input_file_name', fname)

def main():
    #os.chdir(path)
    #performs tunnel_revtun_ver00_gui.sce functionality
    #os.system("sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 tunnel_revtun_SWC_CAB.elf")
    returncode = -1
    RASPPATH = os.getenv("RASPPATH", "/home/ubuntu/rasp30")
    
    program('tunnel_revtun_SWC_CAB.elf')
    write_mem2_NoRelease('0x5500', 'switch_info')
    write_mem2_NoRelease('0x7000', 'switch_info')
    program('switch_program.elf')

    #performs target_program_ver02_gui.sce functionality
    TL = open('target_list', 'r') # open target_list
    n_target_tunnel_revtun=TL.readline() # store values in variables
    n_target_highaboveVt_swc=TL.readline()
    n_target_highaboveVt_ota=TL.readline()
    n_target_aboveVt_swc=TL.readline()
    n_target_aboveVt_ota=TL.readline()
    n_target_aboveVt_otaref=TL.readline()
    n_target_aboveVt_mite=TL.readline()
    n_target_aboveVt_dirswc=TL.readline()
    n_target_subVt_swc=TL.readline()
    n_target_subVt_ota=TL.readline()
    n_target_subVt_otaref=TL.readline()
    n_target_subVt_mite=TL.readline()
    n_target_subVt_dirswc=TL.readline()
    n_target_lowsubVt_swc=TL.readline()
    n_target_lowsubVt_ota=TL.readline()
    n_target_lowsubVt_otaref=TL.readline()
    n_target_lowsubVt_mite=TL.readline()
    n_target_lowsubVt_dirswc=TL.readline()

    if n_target_highaboveVt_swc != OFF:
        write_mem2_NoRelease('0x7000', 'target_info_highaboveVt_swc')
        write_mem2_NoRelease('0x6800', 'pulse_width_table_highaboveVt_swc')
        program('recover_inject_highaboveVt_SWC.elf')
        write_mem2_NoRelease('0x7000', 'target_info_highaboveVt_swc')
        program('first_coarse_program_highaboveVt_SWC.elf')
        write_mem2_NoRelease('0x7000', 'target_info_highaboveVt_swc')
        program('measured_coarse_program_highaboveVt_SWC.elf')
        write_mem2_NoRelease('0x7000', 'target_info_highaboveVt_swc')
        write_mem2_NoRelease('0x6800', 'Vd_table_30mV')
        program('fine_program_highaboveVt_m_ave_04_SWC.elf')

    if n_target_aboveVt_swc != OFF:
        write_mem2_NoRelease('0x7000', 'target_info_aboveVt_swc')
        write_mem2_NoRelease('0x6800', 'pulse_width_table_swc')
        program('recover_inject_aboveVt_SWC.elf')
        write_mem2_NoRelease('0x7000', 'target_info_aboveVt_swc')
        program('first_coarse_program_aboveVt_SWC.elf')
        write_mem2_NoRelease('0x7000', 'target_info_aboveVt_swc')
        program('measured_coarse_program_aboveVt_SWC.elf')
        write_mem2_NoRelease('0x7000', 'target_info_aboveVt_swc')
        write_mem2_NoRelease('0x6800', 'Vd_table_30mV')
        program('fine_program_aboveVt_m_ave_04_SWC.elf')

    if n_target_subVt_swc != OFF:
        write_mem2_NoRelease('0x7000', 'target_info_subVt_swc')
        write_mem2_NoRelease('0x6800', 'pulse_width_table_swc')
        program('recover_inject_subVt_SWC.elf')
        write_mem2_NoRelease('0x7000', 'target_info_subVt_swc')
        program('first_coarse_program_subVt_SWC.elf')
        write_mem2_NoRelease('0x7000', 'target_info_subVt_swc')
        program('measured_coarse_program_subVt_SWC.elf')
        write_mem2_NoRelease('0x7000', 'target_info_subVt_swc')
        write_mem2_NoRelease('0x6800', 'Vd_table_30mV')
        program('fine_program_subVt_m_ave_04_SWC.elf')

    if n_target_lowsubVt_swc != OFF:
        write_mem2_NoRelease('0x7000', 'target_info_lowsubVt_swc')
        write_mem2_NoRelease('0x6800', 'pulse_width_table_lowsubVt_swc')
        program('recover_inject_lowsubVt_SWC.elf')
        write_mem2_NoRelease('0x7000', 'target_info_lowsubVt_swc')
        program('first_coarse_program_lowsubVt_SWC.elf')
        write_mem2_NoRelease('0x7000', 'target_info_lowsubVt_swc')
        program('measured_coarse_program_lowsubVt_SWC.elf')
        write_mem2_NoRelease('0x7000', 'target_info_lowsubVt_swc')
        write_mem2_NoRelease('0x6800', 'Vd_table_30mV')
        program('fine_program_lowsubVt_m_ave_04_SWC.elf')

    if n_target_highaboveVt_ota != OFF:
        write_mem2_NoRelease('0x7000', 'target_info_highaboveVt_ota')
        write_mem2_NoRelease('0x6800', 'pulse_width_table_highaboveVt_ota')
        program('recover_inject_highaboveVt_CAB_ota.elf')
        write_mem2_NoRelease('0x7000', 'target_info_highaboveVt_ota')
        program('first_coarse_program_highaboveVt_CAB_ota.elf')
        write_mem2_NoRelease('0x7000', 'target_info_highaboveVt_ota')
        program('measured_coarse_program_highaboveVt_CAB_ota.elf')
        write_mem2_NoRelease('0x7000', 'target_info_highaboveVt_ota')
        write_mem2_NoRelease('0x6800', 'Vd_table_30mV')
        program('fine_program_highaboveVt_m_ave_04_CAB_ota.elf')

    if n_target_aboveVt_ota != OFF:
        write_mem2_NoRelease('0x7000', 'target_info_aboveVt_ota')
        write_mem2_NoRelease('0x6800', 'pulse_width_table_ota')
        program('recover_inject_aboveVt_CAB_ota.elf')
        write_mem2_NoRelease('0x7000', 'target_info_aboveVt_ota')
        program('first_coarse_program_aboveVt_CAB_ota.elf')
        write_mem2_NoRelease('0x7000', 'target_info_aboveVt_ota')
        program('measured_coarse_program_aboveVt_CAB_ota.elf')
        write_mem2_NoRelease('0x7000', 'target_info_aboveVt_ota')
        write_mem2_NoRelease('0x6800', 'Vd_table_30mV')
        program('fine_program_aboveVt_m_ave_04_CAB_ota.elf')

    if n_target_subVt_ota != OFF:
        write_mem2_NoRelease('0x7000', 'target_info_subVt_ota')
        write_mem2_NoRelease('0x6800', 'pulse_width_table_ota')
        program('recover_inject_subVt_CAB_ota.elf')
        write_mem2_NoRelease('0x7000', 'target_info_subVt_ota')
        program('first_coarse_program_subVt_CAB_ota.elf')
        write_mem2_NoRelease('0x7000', 'target_info_subVt_ota')
        program('measured_coarse_program_subVt_CAB_ota.elf')
        write_mem2_NoRelease('0x7000', 'target_info_subVt_ota')
        write_mem2_NoRelease('0x6800', 'Vd_table_30mV')
        program('fine_program_subVt_m_ave_04_CAB_ota.elf')

    if n_target_lowsubVt_ota != OFF:
        write_mem2_NoRelease('0x7000', 'target_info_lowsubVt_ota')
        write_mem2_NoRelease('0x6800', 'pulse_width_table_lowsubVt_ota')
        program('recover_inject_lowsubVt_CAB_ota.elf')
        write_mem2_NoRelease('0x7000', 'target_info_lowsubVt_ota')
        program('first_coarse_program_lowsubVt_CAB_ota.elf')
        write_mem2_NoRelease('0x7000', 'target_info_lowsubVt_ota')
        program('measured_coarse_program_lowsubVt_CAB_ota.elf')
        write_mem2_NoRelease('0x7000', 'target_info_lowsubVt_ota')
        write_mem2_NoRelease('0x6800', 'Vd_table_30mV')
        program('fine_program_lowsubVt_m_ave_04_CAB_ota.elf')

    if n_target_aboveVt_otaref != OFF:
        write_mem2_NoRelease('0x7000', 'target_info_aboveVt_otaref')
        write_mem2_NoRelease('0x6800', 'pulse_width_table_otaref')
        program('recover_inject_aboveVt_CAB_ota_ref.elf')
        write_mem2_NoRelease('0x7000', 'target_info_aboveVt_otaref')
        program('first_coarse_program_aboveVt_CAB_ota_ref.elf')
        write_mem2_NoRelease('0x7000', 'target_info_aboveVt_otaref')
        program('measured_coarse_program_aboveVt_CAB_ota_ref.elf')
        write_mem2_NoRelease('0x7000', 'target_info_aboveVt_otaref')
        write_mem2_NoRelease('0x6800', 'Vd_table_30mV')
        program('fine_program_aboveVt_m_ave_04_CAB_ota_ref.elf')

    if n_target_subVt_otaref != OFF:
        write_mem2_NoRelease('0x7000', 'target_info_subVt_otaref')
        write_mem2_NoRelease('0x6800', 'pulse_width_table_otaref')
        program('recover_inject_subVt_CAB_ota_ref.elf')
        write_mem2_NoRelease('0x7000', 'target_info_subVt_otaref')
        program('first_coarse_program_subVt_CAB_ota_ref.elf')
        write_mem2_NoRelease('0x7000', 'target_info_subVt_otaref')
        program('measured_coarse_program_subVt_CAB_ota_ref.elf')
        write_mem2_NoRelease('0x7000', 'target_info_subVt_otaref')
        write_mem2_NoRelease('0x6800', 'Vd_table_30mV')
        program('fine_program_subVt_m_ave_04_CAB_ota_ref.elf')

    if n_target_lowsubVt_otaref != OFF:
        write_mem2_NoRelease('0x7000', 'target_info_lowsubVt_otaref')
        write_mem2_NoRelease('0x6800', 'pulse_width_table_lowsubVt_otaref')
        program('recover_inject_lowsubVt_CAB_ota_ref.elf')
        write_mem2_NoRelease('0x7000', 'target_info_lowsubVt_otaref')
        program('first_coarse_program_lowsubVt_CAB_ota_ref.elf')
        write_mem2_NoRelease('0x7000', 'target_info_lowsubVt_otaref')
        program('measured_coarse_program_lowsubVt_CAB_ota_ref.elf')
        write_mem2_NoRelease('0x7000', 'target_info_lowsubVt_otaref')
        write_mem2_NoRelease('0x6800', 'Vd_table_30mV')
        program('fine_program_lowsubVt_m_ave_04_CAB_ota_ref.elf')

    if n_target_aboveVt_mite != OFF:
        write_mem2_NoRelease('0x7000', 'target_info_aboveVt_mite')
        write_mem2_NoRelease('0x6800', 'pulse_width_table_mite')
        program('recover_inject_aboveVt_CAB_mite.elf')
        write_mem2_NoRelease('0x7000', 'target_info_aboveVt_mite')
        program('first_coarse_program_aboveVt_CAB_mite.elf')
        write_mem2_NoRelease('0x7000', 'target_info_aboveVt_mite')
        program('measured_coarse_program_aboveVt_CAB_mite.elf')
        write_mem2_NoRelease('0x7000', 'target_info_aboveVt_mite')
        write_mem2_NoRelease('0x6800', 'Vd_table_30mV')
        program('fine_program_aboveVt_m_ave_04_CAB_mite.elf')

    if n_target_subVt_mite != OFF:
        write_mem2_NoRelease('0x7000', 'target_info_subVt_mite')
        write_mem2_NoRelease('0x6800', 'pulse_width_table_mite')
        program('recover_inject_subVt_CAB_mite.elf')
        write_mem2_NoRelease('0x7000', 'target_info_subVt_mite')
        program('first_coarse_program_subVt_CAB_mite.elf')
        write_mem2_NoRelease('0x7000', 'target_info_subVt_mite')
        program('measured_coarse_program_subVt_CAB_mite.elf')
        write_mem2_NoRelease('0x7000', 'target_info_subVt_mite')
        write_mem2_NoRelease('0x6800', 'Vd_table_30mV')
        program('fine_program_subVt_m_ave_04_CAB_mite.elf')

    if n_target_lowsubVt_mite != OFF:
        write_mem2_NoRelease('0x7000', 'target_info_lowsubVt_mite')
        write_mem2_NoRelease('0x6800', 'pulse_width_table_lowsubVt_mite')
        program('recover_inject_lowsubVt_CAB_mite.elf')
        write_mem2_NoRelease('0x7000', 'target_info_lowsubVt_mite')
        program('first_coarse_program_lowsubVt_CAB_mite.elf')
        write_mem2_NoRelease('0x7000', 'target_info_lowsubVt_mite')
        program('measured_coarse_program_lowsubVt_CAB_mite.elf')
        write_mem2_NoRelease('0x7000', 'target_info_lowsubVt_mite')
        write_mem2_NoRelease('0x6800', 'Vd_table_30mV')
        program('fine_program_lowsubVt_m_ave_04_CAB_mite.elf')

    if n_target_aboveVt_dirswc != OFF:
        write_mem2_NoRelease('0x7000', 'target_info_aboveVt_dirswc')
        write_mem2_NoRelease('0x6800', 'pulse_width_table_dirswc')
        program('recover_inject_aboveVt_DIRSWC.elf')
        write_mem2_NoRelease('0x7000', 'target_info_aboveVt_dirswc')
        program('first_coarse_program_aboveVt_DIRSWC.elf')
        write_mem2_NoRelease('0x7000', 'target_info_aboveVt_dirswc')
        program('measured_coarse_program_aboveVt_DIRSWC.elf')
        write_mem2_NoRelease('0x7000', 'target_info_aboveVt_dirswc')
        write_mem2_NoRelease('0x6800', 'Vd_table_30mV')
        program('fine_program_aboveVt_m_ave_04_DIRSWC.elf')

    if n_target_subVt_dirswc != OFF:
        write_mem2_NoRelease('0x7000', 'target_info_subVt_dirswc')
        write_mem2_NoRelease('0x6800', 'pulse_width_table_dirswc')
        program('recover_inject_subVt_DIRSWC.elf')
        write_mem2_NoRelease('0x7000', 'target_info_subVt_dirswc')
        program('first_coarse_program_subVt_DIRSWC.elf')
        write_mem2_NoRelease('0x7000', 'target_info_subVt_dirswc')
        program('measured_coarse_program_subVt_DIRSWC.elf')
        write_mem2_NoRelease('0x7000', 'target_info_subVt_dirswc')
        write_mem2_NoRelease('0x6800', 'Vd_table_30mV')
        program('fine_program_subVt_m_ave_04_DIRSWC.elf')

    if n_target_lowsubVt_dirswc != OFF:
        write_mem2_NoRelease('0x7000', 'target_info_lowsubVt_dirswc')
        write_mem2_NoRelease('0x6800', 'pulse_width_table_lowsubVt_dirswc')
        program('recover_inject_lowsubVt_DIRSWC.elf')
        write_mem2_NoRelease('0x7000', 'target_info_lowsubVt_dirswc')
        program('first_coarse_program_lowsubVt_DIRSWC.elf')
        write_mem2_NoRelease('0x7000', 'target_info_lowsubVt_dirswc')
        program('measured_coarse_program_lowsubVt_DIRSWC.elf')
        write_mem2_NoRelease('0x7000', 'target_info_lowsubVt_dirswc')
        write_mem2_NoRelease('0x6800', 'Vd_table_30mV')
        program('fine_program_lowsubVt_m_ave_04_DIRSWC.elf')

    TL.close()

    write_mem2_NoRelease('0x4300', 'input_vector')
    write_mem2_NoRelease('0x4200', 'output_info')
    write_mem2_NoRelease('0x5500', 'gpin_vector')

    exec_command('run_new.tcl -speed 115200', 'voltage_meas.elf')
    os.system("sleep 2")

    exec_command('read_mem2_NoRelease.tcl -start_address 0x6000 -length 1000 -output_file_name', 'output_vector')
    os.system("sleep 2")
