"""This module is main module for contestant's solution."""

from hackathon.utils.control import Control
from hackathon.utils.utils import ResultsMessage, DataMessage, PVMode, \
    TYPHOON_DIR, config_outs
from hackathon.framework.http_server import prepare_dot_dir

def worker(msg: DataMessage) -> ResultsMessage:

    load_one_my=True
    load_two_my=True
    load_three_my=True
    power_reference_my=0.0
    pv_mode_my=PVMode.ON


    how_much_i_must_use=msg.current_load- msg.solar_production
    how_much_energy_battery_has=600*msg.bessSOC

    if msg.grid_status:
        if msg.buying_price == 3:

            if how_much_energy_battery_has < 600:
                if how_much_energy_battery_has < 300:
                    power_reference_my = - how_much_i_must_use * 4
                else:
                    power_reference_my = - how_much_i_must_use * 2
            else:
                power_reference_my = - how_much_i_must_use
        elif msg.buying_price == 8 and msg.current_load > 5.0: #5
            energy_of_load3=how_much_i_must_use*0.3
            load_three_my=False
            power_reference_my=msg.current_load-how_much_i_must_use*0.3
        else:
            if_buttery_stil_has_energy=how_much_energy_battery_has-how_much_i_must_use
            if if_buttery_stil_has_energy < 450:
                print ("usao manje od 450")
            elif if_buttery_stil_has_energy < 300:
                power_reference_my=how_much_i_must_use-300
            elif  if_buttery_stil_has_energy < 150:
                power_reference_my=how_much_i_must_use-400
            if if_buttery_stil_has_energy>0:
                power_reference_my=how_much_i_must_use
            else:
                if if_buttery_stil_has_energy+5>600:
                    power_reference_my=if_buttery_stil_has_energy-3
                else:
                    power_reference_my=if_buttery_stil_has_energy-5

    else:
        if_buttery_stil_has_energy=how_much_energy_battery_has-how_much_i_must_use
        if if_buttery_stil_has_energy>0:
            power_reference_my=how_much_i_must_use
        else:
            energy_of_load1=how_much_i_must_use*0.2
            energy_of_load2=how_much_i_must_use*0.5
            energy_of_load3=how_much_i_must_use*0.3
            if_buttery_stil_has_energy=how_much_energy_battery_has-energy_of_load1

            if if_buttery_stil_has_energy < 0:
                load_one_my=False
                load_two_my=False
                load_three_my=False
                power_reference_my=0;
            if_buttery_stil_has_energy2=if_buttery_stil_has_energy-energy_of_load2
            if if_buttery_stil_has_energy2 > 0:
                    power_reference_my=energy_of_load2+energy_of_load1
                    load_three_my=False
            else:
                 load_two_my=False
                 if_buttery_stil_has_energy3=if_buttery_stil_has_energy-energy_of_load3
                 if if_buttery_stil_has_energy2 > 0:
                         power_reference_my=energy_of_load3+energy_of_load1
                 else:
                    load_three_my=False
                    power_reference_my=energy_of_load1


    # Dummy result is returned in every cycle here
    return ResultsMessage(data_msg=msg,
                          load_one=load_one_my,
                          load_two=load_two_my,
                          load_three=load_three_my,
                          power_reference=power_reference_my,
                          pv_mode=pv_mode_my)


def run(args) -> None:
    prepare_dot_dir()
    config_outs(args, 'solution')

    cntrl = Control()

    for data in cntrl.get_data():
        cntrl.push_results(worker(data))
