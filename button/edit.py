import app, active, utils, dir, lib

import os, copy, guizero
# Change Cover Button
def change_cover():
    os.chdir(dir.img_root)
    new_cover_path = app.main.app.select_file()
    if new_cover_path == '':
        return
    cover_file_name = active.edit.obj.images[0]
    utils.files.copyFile(new_cover_path, dir.temp_img, cover_file_name)
    app.edit.cover_image.image = copy.copy(os.path.join(dir.temp_img, cover_file_name))

# Multifandom Checkbox
def multifandom_checkbox_pressed():
    # Multifandom -> Single Fandom
    if app.edit.multifandom_checkbox.value == 0:
        new_fandom = guizero.question('Convert Multifandom to Singlefandom Anthology', 'Are you sure you want to do this?', initial_value='Fandom Name')
        # If you cancel the action, set the checkbox back to 1
        if new_fandom == None:
            app.edit.multifandom_checkbox.value = 1
            return
        else:
            active.edit.obj = utils.obj.convertSingleFandom(new_fandom, active.edit.obj)
            active.index.page.update(0)
            app.edit.update()
    # Single Fandom -> Multifandom
    else:
        if guizero.yesno('Convert Singlefandom to Multifandom Anthology', 'Are you sure you want to do this?'):
            edit_fandoms()
        # if closed without doing anything, turn checkbox back to 0
        else:
            app.edit.multifandom_checkbox.value = 0
            return

def edit_fandoms():
    active.fan.update(copy.deepcopy(active.edit).obj)
    app.edit.screen.disable()
    app.fan.window.show(wait=True)
    lib.load_fan_misc_library()
    app.fan.update()

def edit_works():
    # active.copy.clone('cont')
    # gui.cont.update()
    # data.cont.grab()
    return

def edit_images():
    # Add Functionality
    return

