class Wash_Hands():
    def turn_on_tap_water():
        event = "I can safely touch a light switch."
        event.precondition = ("hands", "dry")
    def put_hands_under_running_water():
        event = "I can safely touch a light switch."
        event.precondition = ("hands", "dry")
    def apply_soap_and_rub_hands():
        event = "I can safely touch a light switch."
        event.precondition = ("hands", "dry")
    def turn_off_the_tap_water():
        event = "I can safely touch a light switch."
        event.precondition = ("hands", "dry")
    def dry_my_hands_using_towel():
        event = "I can safely touch a light switch."
        event.precondition = ("hands", "dry")


class Wash_Hands():
    def turn_on_the_tap_water():
        event = "Water streaming sound can be heard."
        event.precondition = ("water", "running")
    def put_hands_under_running_water():
        event = "Water streaming sound can be heard."
        event.precondition = ("water", "running")
    def apply_soap_and_rub_hands():
        event = "Water streaming sound can be heard."
        event.precondition = ("water", "running")
    def turn_off_the_tap_water():
        event = "Water streaming sound can be heard."
        event.precondition = ("water", "running")
    def dry_my_hands_using_a_towel():
        event = "Water streaming sound can be heard."
        event.precondition = ("water", "running")


class Change_Battery_Of_TV_Remote_Control():
    def pop_open_the_battery_cover():
        event = "I can see inside the battery compartment."
        event.precondition = ("battery cover", "open")
    def take_out_the_old_batteries():
        instruction = "Take out the old batteries."
        event = "I can see inside the battery compartment."
        event.precondition = ("battery cover", "open")
    def put_in_new_batteries():
        event = "I can see inside the battery compartment."
        event.precondition = ("battery cover", "open")
    def close_battery_cover():
        event = "I can see inside the battery compartment."
        event.precondition = ("battery cover", "open")

class Change_Battery_Of_TV_Remote_Control():
    def pop_open_battery_cover():
        event = "The remote can turn on a TV."
        event.precondition = ("remote", "has battery")
    def take_ouy_old_batteries():
        event = "The remote can turn on a TV."
        event.precondition = ("remote", "has battery")
    def put_in_new_batteries():
        event = "The remote can turn on a TV."
        event.precondition = ("remote", "has battery")
    def close_battery_cover():
        event = "The remote can turn on a TV."
        event.precondition = ("remote", "has battery")
        
class Cook_Salmon_In_Oven():
    def pat_dry_salmon():
        event = "I touch the salmon and my fingers get wet."
        event.precondition = ("salmon surface", "wet")
    def brush_salmon_with_sauce():
        event = "I touch the salmon and my fingers get wet."
        event.precondition = ("salmon surface", "wet")
    def put_salmon_on_foil():
        event = "I touch the salmon and my fingers get wet."
        event.precondition = ("salmon surface", "wet")
    def put_salmon_in_oven_preheated_to_350_degress_for_20_minutes():
        event = "I touch the salmon and my fingers get wet."
        event.precondition = ("salmon surface", "wet")
    def serve_salmon():
        event = "I touch the salmon and my fingers get wet."
        event.precondition = ("salmon surface", "wet")

class Cook_Salmon_In_Oven():
    def pat_dry_salmon():
        event = "The salmon can be easliy flaked by a fork."
        event.precondition = ("salmon", "cooked")
    def brush_salmon_with_sauce():
        event = "The salmon can be easliy flaked by a fork."
        event.precondition = ("salmon", "cooked")
    def put_salmon_on_foil():
        event = "The salmon can be easliy flaked by a fork."
        event.precondition = ("salmon", "cooked")
    def put_salmon_in_oven_preheated_to_350_degrees_for_20_minutes():
        event = "The salmon can be easliy flaked by a fork."
        event.precondition = ("salmon", "cooked")
    def serve_salmon():
        event = "The salmon can be easliy flaked by a fork."
        event.precondition = ("salmon", "cooked")


