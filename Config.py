class Config:

    delay = 600

    headless_is_available = True

    start_url = "https://www.xing.com/"
    logged_in_url = "https://www.xing.com/app/startpage"
    contacts_url = "https://www.xing.com/contacts"

    contacts_unconfirmed_url = "https://www.xing.com/app/contact?op=toconfirm"
    contacts_unconfirmed_section_xpath = "//*[contains(@class, 'item clfx medium-img more-actions')]"
    contacts_unconfirmed_section_subclass_username_xpath = ".//*[contains(@class, 'component-user-name component-user-name-15')]"
    contacts_unconfirmed_section_subclass_company_xpath = ".//*[contains(@class, 'company')]"
    contacts_unconfirmed_confirm_deletion_form_xpath = "//*[contains(@class, 'delete-contact-form')]"
    contacts_unconfirmed_confirm_deletion_frame_id = "delete-contact-lightbox"
    contacts_unconfirmed_section_subclass_delete_xpath = ".//*[contains(@class, 'icon-links icn-ext-ctr-delete')]"
    contacts_unconfirmed_confirm_deletion_xpath = ".//*[contains(@class, 'element-form-button-solid-lime')]"

    contacts_recommended_url = "https://www.xing.com/contacts/recommendations"
    contacts_recommended_card_xpath = ".//*[contains(@class, 'reco-card') and not(contains(@class, 'teaser-card'))]"
    contacts_recommended_add_button_xpath = ".//*[contains(@class, 'element-form-button-solid-lime')]"
    contacts_recommended_username_xpath = ".//*[contains(@class, 'user-name')]"

    login_button_id = "login-trigger"
    login_form_username_name = "login_form[username]"
    login_form_password_name = "login_form[password]"

    requests_per_batch = 5
    load_delay = 5
    login_delay = 10
    exception_delay = 5
    request_delay = 5
    unrequest_delay = 5
