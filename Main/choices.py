#FILE CONTAINING ALL PROCESS, SUB PROCESS, MACHINE SENSOR AND INPUT CHOICES 

"""
PROCESS_CHOICES = [
	('','Choose a Process'),
	('incoming_goods', 'Incoming Goods'),
	('store_material', 'Store Material'),
	('move_material', 'Move Material to Ply Cutting'),
	('cut_plies', 'Cut Plies'),
	('inspect_plies', 'Inspect Plies'),
	('sort_plies', 'Sort Plies'),
	('create_blanks', 'Create Stabilised Blanks'),
	('form_preform', 'Form Preform'),
]
process_dict = {
	'incoming_goods': 'Incoming Goods',
	'store_material': 'Store Material',
	'move_material': 'Move Material to Ply Cutting',
	'cut_plies': 'Cut Plies',
	'inspect_plies': 'Inspect Plies',
	'sort_plies': 'Sort Plies',
	'create_blanks': 'Create Stabilised Blanks',
	'form_preform': 'Form Preform',
	}
	
MANUAL_PROCESS_CHOICES = [
	('','Choose a Process'),
	('incoming_goods', 'Incoming Goods'),
	('store_material', 'Store Material'),
	('move_material', 'Move Material to Ply Cutting'),
	('cut_plies', 'Cut Plies'),
	('inspect_plies', 'Inspect Plies'),
	('sort_plies', 'Sort Plies'),
	('create_blanks', 'Create Stabilised Blanks'),
	('form_preform', 'Form Preform'),
]
manual_process_dict = {
	'incoming_goods': 'Incoming Goods',
	'store_material': 'Store Material',
	'move_material': 'Move Material to Ply Cutting',
	'cut_plies': 'Cut Plies',
	'inspect_plies': 'Inspect Plies',
	'sort_plies': 'Sort Plies',
	'create_blanks': 'Create Stabilised Blanks',
	'form_preform': 'Form Preform',
	}

SUB_PROCESS_CHOICES = [
	('init', 'Initialisation'),
	('material_loaded', 'Material loaded in machine'),
	('platten_init', 'Platten at initial location'),
	('material_tool_in_press', 'Material and Tool Inside Press'),
	('material_pressed', 'Material Pressed'),
	('material_released', 'Material Released from Tool'),
	('machine_init', 'Machine Returns To Initial Locations'),
	('remover_on', 'Removal End effector actuated'),
	('pre_form_gone', 'Preform leaves Tool'),
	('final_inspection', 'Final Inspection'),
]
sub_process_dict = {
	'init' : 'Initialisation',
	'material_loaded' : 'Material loaded in machine',
	'platten_init' : 'Platten at initial location',
	'material_tool_in_press' : 'Material and Tool Inside Press',
	'material_pressed' : 'Material Pressed',
	'material_released' : 'Material Released from Tool',
	'machine_init' : 'Machine Returns To Initial Locations',
	'remover_on' : 'Removal End effector actuated',
	'pre_form_gone' : 'Preform leaves Tool',
	'final_inspection' : 'Final Inspection',
}

MANUAL_SUB_PROCESS_CHOICES = [
	
	('material_loaded', 'Material loaded in machine'),
	
	('material_tool_in_press', 'Material and Tool Inside Press'),
	('material_pressed', 'Material Pressed'),
	('remover_on', 'Removal End effector actuated'),
	('material_released', 'Material Released from Tool'),
	('final_inspection', 'Final Inspection'),
]
manual_sub_process_dict = {
	'material_loaded' : 'Material loaded in machine',
	'material_tool_in_press' : 'Material and Tool Inside Press',
	'material_pressed' : 'Material Pressed',
	'remover_on': 'Removal End effector actuated',
	'material_released' : 'Material Released from Tool',
	'final_inspection' : 'Final Inspection',
}

COMPANY_CHOICES = [
	('airborne','Airborne'),
	('test_comp','Test Company'),
]
company_choices_dict = {
'airborne' : 'Airborne',
'test_comp' : 'Test Company'
}

PRO_SENSOR_CHOICES = [	
	('qr_code','QR Code'),
	('rth','RTH'),
	('L515','L515'),
	('D455','D455'),
	('VOC','VOC Sensor'),
	('DUS','Dust Sensor'),
	('HUS','Humidity Sensor'),
	('accelerometer', 'Accelerometer'),
	('strain_gauge', 'Strain Gauge'),
	('microphone', 'Microphone'),
	('thermocouple', 'Thermocouple'),

	
]

pro_sensor_choices_dict = {
	'qr_code':'QR Code',
	'rth':'RTH',
	'L515':'L515',
	'D455':'D455',
	'VOC':'VOC Sensor',
	'DUS':'Dust Sensor',
	'HUS':'Humidity Sensor',
	'accelerometer': 'Accelerometer',
	'strain_gauge': 'Strain Gauge',
	'microphone':'Microphone',
	'thermocouple':'Thermocouple',

}

SENSOR_CHOICES = [
	('L515','L515'),
	('D455','D455'),
	('thermocouple', 'Thermocouple'),
	('timer', 'Timer'),
	('loc_sw', 'Location Switch'),
	('accelerometer', 'Accelerometer'),
	('motor', 'Motor Driver'),
	('microphone', 'Microphone'),
	('encoder','Encoder'),
	('pistons_loc','Pistons Location Switch'),
	('strain_gauge', 'Strain Gauge'),
	('scale','Scale'),
	('pressure','Pressure Sensor'),
]
sensor_choices_dict = {
	'L515':'L515',
	'D455':'D455',
	'thermocouple':'Thermocouple',
	'timer':'Timer',
	'loc_sw':'Location Switch',
	'accelerometer':'Accelerometer',
	'motor':'Motor Driver',
	'microphone':'Microphone',
	'encoder':'Encoder',
	'pistons':'Pistons',
	'pistons_loc':'Pistons Location Switch',
	'halo':'Halo',
	'reflective':'Reflective Sensor',
	'pos_sensor':'Positional Sensor',
	'strain_gauge':'Strain Gauge',
	'scale':'Scale',
	'pressure' : 'Pressure Sensor',
}


MACHINE_CHOICES = [
	('ply_cutter','Ply Cutter'),
	('pick_place_sort','Pick and Place (sort)'),
	('pick_place_blanks','Pick and Place (blanks)'),
	('preform_cell', 'Preforming Cell'),
]
machine_choices_dict = {
	'ply_cutter':'Ply Cutter',
	'pick_place_sort':'Pick and Place (sort)',
	'pick_place_blanks':'Pick and Place (blanks)',
	'preform_cell':'Preforming Cell',
}


MANUAL_INPUT_CHOICES = [
('LAB','	Labour Input'),
('SCR','	Scrap Rate'),
('BAT','	Batch Size'),
('POR','	Power Consumption'),
('BPN','	Baseline Part Number'),
('CO2', '	CO2 emissions from power'),
]
manual_input_dict = {
'LAB' : 'labourInput',
'SCR' : 'scrapRate',
'BAT' : 'batchSize',
'POR' : 'power',
'BPN' : 'baseLinePartNo',
'CO2' : 'CO2',
}

MANUAL_INPUT_TIME_CHOICES = [
('JBS','	Job Start Time'),
('JBE','	Job End Time'),
]

manual_input_time_dict = {
'JBS' : 'jobStart',
'JBE' : 'jobEnd',
}

CONST_CHOICES = [
('MPM','	Material Price Per m^2'),
('MPK','	Material Price Per Kilo'),
('MAD','	Material Density'),
('THR','	Technician Rate'),
('SUR','	Supervisor Rate'),
('TLH','	Technician Labour Hours'),
('SLH','	Supervisor Labour Hours'),
('PWR','	Electricity Rate'),
('NPW','	Nominal Part Weight'),
('NPL','	Nominal Length'),
('NWI','	Nominal Width'),
('NPT','	Nominal Thickness'),
('SUC','	Set Up Cost'),

]

const_dict = {
'MPM':'priceM2',
'MPK':'priceKG',
'MAD':'materialDensity',
'THR':'techRate',
'SUR':'superRate',
'PWR':'powerRate',
'TLH':'techLabourHours',
'SLH':'superLabourHours',
'NPW':'nominalPartWeight',
'NPL':'nominalPartLength',
'NWI':'nominalPartWidth',
'NPT':'nominalPartThickness',
'SUC':'setUpCost',
}

SUB_TOLERANCE_CHOICES = [
('LET',' Length Tolerance'),
('WDT',' Width Tolerance'),
('DET',' Depth Tolerance'),
]

sub_tolerance_dict = {
	'LET':'sublengthTolerance',
	'WDT':'subwidthTolerance',
	'DET':'subdepthTolerance',
}

INSPECT_CHOICES = [
('WET',' Weight Tolerance'),
('LET',' Length Tolerance'),
('WDT',' Width Tolerance'),
('DET',' Depth Tolerance'),
]

inspect_dict = {
	'WET':'subweightTolerance',
	'LET':'sublengthTolerance',
	'WDT':'subwidthTolerance',
	'DET':'subdepthTolerance',
}

#Individual Sub Process Choice Lists and Dictionaires 

MATERIAL_IN_PRESS_CHOICES = [
('CPT', 'Centre Position at tension frame'),
('CPMT', 'Centre position at male tool'),
('T', 'Tolerance'),
]


material_in_press_dict = {
	'CPT':'centrePosT',
	'CPMT': 'centrePosMT',
	'T': 'tolerance',

}

MATERIAL_PRESSED_CHOICES = [
	('TEMP', 'Temperature'),
	('PR', 'Pressure'),
	('TI', 'Time'),
]

material_pressed_dict = {
	'TEMP': 'temperature',
	'PR': 'pressure',
	'TI': 'time',
}

REMOVAL_EFFECTOR_CHOICES = [
	('VP', 'Vertical position of end effector'),
	('x2', 'Tolerance'),
]

removal_effector_dict = {
	'VP': 'verticalEffector',
	'PR': 'tolerancex2',
}

TRIMMING_CHOICES = [
	('TT', 'Thickness Tolerance'),
	('NW','Nominal width'),
	('NL','Nominal length'),
	('NT','Nominal thickness'),
	('WT','Width tolerance'),
	('LT','Length tolerance'),
	('DT','Depth tolerance'),
	('NPW','Nominal preform weight'),
	('TW','Weight Tolerance'),
	('NVW','Nominal volume of wrinkling'),
	('PWT','Preform wrinkling tolerance'),
]

trimming_dict = {
	'TT': 'thicknessTolerance',
	'NW':'nominalWidth',
	'NL':'nominalLength',
	'NT':'nominalThickness',
	'WT':'subwidthTolerance',
	'LT':'sublengthTolerance',
	'DT':'subdepthTolerance',
	'NPW':'nominalPreformWeight',
	'TW':'subweightTolerance',
	'NVW':'nominalVolumeWrinkling',
	'PWT':'preformWrinklingTolerance',
}


"""




