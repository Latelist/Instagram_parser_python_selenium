import view.inputs
import model.open_instagram
import model.collect_data
import model.json_saver
import model.csv_saver
import model.create_files

def controller():
    view.inputs.greeting_message() #пользователь нажимает Enter, чтобы продолжить
    driver = model.open_instagram.start_driver()

    IG_username, IG_password = model.open_instagram.load_login_data()

    model.open_instagram.login_auto(driver, IG_username, IG_password) #логиним пользователя автоматически. Если не залогинился, пробуем логинить вручную
    if model.open_instagram.is_logged_in(driver):
        view.inputs.show_login_success()
    else:
        view.inputs.login_instructions()
        model.open_instagram.login_manually(driver)
        while not model.open_instagram.is_logged_in(driver):
            view.inputs.show_login_failure()
        view.inputs.show_login_success()
    
    while True: 
        URL = view.inputs.ask_for_URL()
        
        try: 
            model.open_instagram.open_profile(driver, URL)

            model.open_instagram.get_username(driver)
            data = model.collect_data.get_profile_data(driver)

            filename_json = model.create_files.make_file_name(data["name"], "json")
            filename_csv = model.create_files.make_file_name(data["name"], "csv")


            model.json_saver.save_data_json(filename_json, data)
            post_links = model.collect_data.get_all_posts(driver)

            for post in post_links:
                post_info = model.collect_data.get_post_info(driver, post)
                model.csv_saver.save_post_to_csv(post_info, filename_csv)
        except:
            print("Драйверу Хрома не удалось открыть профиль. Попробуйте ещё раз")
        
        var = view.inputs.quit()
        if not var:
            driver.quit()
            break
