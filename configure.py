import sys
import getopt
import json
import gc
import os


class Configure:

    def __init__(self):

        status = 'no_config'
        config = {}

        self.load()
        if self.status == 'invalid_config':
            print('Invalid configuration.json file, resetting to original test config.')
            self.reset()
            self.load()
            if self.status == 'invalid_config':
                print('Could not reset configuration.json file.')
                exit()

    def reset(self):
        self.config = {}
        self.config['config_name'] = 'default_afafruit_motor_hat_config'
        self.config['config_description'] = 'Default Afafruit Motor Hat Tank Config'

        self.config['camera_fpv_res_x'] = 1056
        self.config['camera_fpv_res_y'] = 594
        self.config['camera_fpv'] = 'raspberry_pi_8mp'
        self.config['camera_photo_res_x'] = 3280  # for v2, or 2592 for v1
        self.config['camera_photo_res_y'] = 2464  # for v2, or 1944 for v1
        self.config['camera_vflip'] = False
        self.config['camera_hflip'] = False
        self.config['camera'] = 'raspberry_pi_8mp'
        self.config['camera_fpv_path'] = 'static/fpv'
        self.config['camera_fpv_path'] = 'static/fpv'  # This folder gets purged of old images often
        self.config['camera_pictures_path'] = 'static/camera/photos'  # This can be redirected to ? a dropbox folder ?
        self.config['camera_thumbnail_path'] = 'static/camera/thumbnails'

        self.config['sensors'] = 'sensors_none'

        self.config['motor'] = 'adafruit_dc_and_stepper_motor_hat'
        self.config['motor_mode'] = 'tank'
        # Adafruit_MotorHAT:
        #   FORWARD = 1
        #   BACKWARD = 2
        #   BRAKE = 3
        #   RELEASE = 4
        self.config['tank_left_forward'] = 1
        self.config['tank_right_forward'] = 1
        self.config['tank_left_reverse'] = 2
        self.config['tank_right_reverse'] = 2
        self.config['tank_left_motor'] = 1
        self.config['tank_right_motor'] = 2
        self.config['tank_speed_right'] = 155
        self.config['tank_speed_left'] = 145
        self.config['tank_turn_speed'] = 135
        self.config['tank_speed_right_max'] = 255
        self.config['tank_speed_left_max'] = 235

        # Camera Gimbal or Robot Arm
        self.config['servo'] = "adafruit_servo_hat"
        self.config['servo_camera_horz_number'] = -1
        self.config['servo_camera_roll_number'] = -1
        self.config['servo_camera_vert_number'] = 0  # gpio number or servo number dependant on driver
        self.config['servo_camera_vert_bottom'] = 584
        self.config['servo_camera_vert_park'] = 584
        self.config['servo_camera_vert_center'] = 300
        self.config['servo_camera_vert_top'] = 150

        # CSS styles
        self.config['ui_color'] = 'green'
        self.config['ui_size'] = 'lg4'

        # Write the new default config
        config_fh = open('configuration.json', "w")
        config_fh.write(json.dumps(self.config, sort_keys=True, indent=4, separators=(',', ': ')))
        print('Config data saved in configuration.json \n')
        config_fh.close()

    def load(self):
        try:
            config_fh = open("configuration.json", "r")
            json_array_string = str(config_fh.read())
            self.config = json.loads(json_array_string)
            print(' + Config for ' + self.config['config_description'] + ' loaded')
            config_fh.close()
            # print(self.config)
            self.status = 'ready'
        except IOError:
            self.status = 'invalid_config'

    def setup(self):
        return True

    def get_uis_at_startup(self):
        uis = {}

        # Instrument Status
        uis['compass'] = 'disabled'
        uis['tilt'] = 'disabled'
        uis['battery'] = 'disabled'
        uis['thermometer'] = 'disabled'
        uis['sensors'] = 'disabled'
        uis['wifi'] = 'active'
        uis['drive'] = 'disabled'

        # Instrument Values
        uis['direction'] = 'fa-spin'
        uis['charge'] = '2'
        uis['temperature'] = '2'
        return uis

    def get_setting_specifications(self):
        specs_fh = open("setting_specifications.json", "r")
        specs = json.loads(str(specs_fh.read()))
        specs_fh.close()
        return specs

    def get_setting_specifications_for_category(self, category):
        specs_fh = open("setting_specifications.json", "r")
        specs = json.loads(str(specs_fh.read()))
        specs_fh.close()
        cat_specs = {}
        cat_spec_ctr = 0
        for spec in specs.items():
            if spec.category == category:  # FIXME
                cat_specs[cat_spec_ctr] = spec
            cat_spec_ctr += 1
        return cat_specs

    def get_setting_categories(self):
        categories = {}
        categories[0] = {"index": "camera", "title": "Camera Settings"}
        categories[1] = {"index": "motor", "title": "Motor Settings"}
        categories[2] = {"index": "servo", "title": "Servo Settings"}
        categories[3] = {"index": "sensors", "title": "Sensor Settings"}
        return categories

    def update_settings(self, setting_updates, category):
        for setting_name, new_value in setting_updates.items():
            if setting_name == category + "_mode" and not new_value == self.settings[setting_name]:
                # remove old mode specific settings like tank_* if not tank mode anymore
                new_mode = setting_name
                old_mode = self.settings[setting_name]
                for old_mode_setting, old_mode_value in self.get_mode_settings(old_mode):
                    del self.settings[old_mode_setting]
                for new_mode_setting, new_mode_value in self.get_sub_settings_by_mode(self.settings[category], new_mode):
                    self.settings[new_mode_setting] = new_mode_value
                self.settings[category + "_mode"] = new_value
            else:
                self.settings[setting_name] = new_value
        # write the new settings somewhere
        self.save_settings()
        return True

    def get_mode_settings(self, mode):
        mode_settings = {}
        for setting_name, setting_value in self.settings:
            if setting_name.find(mode + "_") == 0:
                mode_settings[setting_name] = setting_value
        return mode_settings

    def get_sub_settings_by_mode(self, mode, category_driver):
        specs_fh = open("setting_specifications.json", "r")
        specs = json.loads(str(specs_fh.read()))
        specs_fh.close()
        driver_specs = specs[category_driver]
        sub_specs = {}
        for spec_name, values in driver_specs.items():
            if spec_name.find(mode + "_") == 0 and 'default' in values and values['type'] == 'int':
                sub_specs[spec_name] = int(values['default'])
            elif spec_name.find(mode + "_") == 0 and 'default' in values and values['type'] == 'float':
                sub_specs[spec_name] = float(values['default'])
            elif spec_name.find(mode + "_") == 0 and 'default' in values:
                sub_specs[spec_name] = values['default']
            elif spec_name.find(mode + "_") == 0:
                sub_specs[spec_name] = 0
        return sub_specs

    def save_settings(self):
        config_fh = open('new_configuration.json', "w")
        config_fh.write(json.dumps(self.settings, sort_keys=True, indent=4, separators=(',', ': ')))
        print('Config data saved in new_configuration.json \n')
        config_fh.close()

    def get_active_driver_settings(self):
        driver_settings = []
        setting_index = 0
        drivers = self.get_drivers()
        specs = self.get_setting_specifications()
        # loop through drivers in specs
        for driver, driver_name in drivers.items():
            # loop through settings in driver
            for setting_name, setting_value in self.config.items():
                # if setting in driver matches one in config, then add it to the list
                if setting_name in specs[driver_name]:
                    next_setting = {}
                    next_setting['name'] = setting_name
                    next_setting['value'] = setting_value
                    next_setting['sort'] = specs[driver_name][setting_name]['sort']
                    driver_settings.append(next_setting)

        # sort by sort field
        print('driver_settings : ' + str(driver_settings))
        return drivers

    def get_drivers(self):
        driver_names = {}
        driver_names[0] = self.config['camera']
        driver_names[1] = self.config['motor']
        driver_names[2] = self.config['servo']
        driver_names[3] = self.config['sensors']
        return driver_names
