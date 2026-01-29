import data
import helpers

from selenium import webdriver
from pages import UrbanRoutesPage


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        # do not modify - we need additional logging enabled in order to retrieve phone confirmation code
        from selenium.webdriver import DesiredCapabilities

        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

        # required: move URL reachability check into setup_class
        if not helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            raise Exception("URL is not reachable")

        # IMPORTANT: use capabilities here (otherwise SMS code retrieval can fail)
        cls.driver = webdriver.Chrome()
        cls.driver.get(data.URBAN_ROUTES_URL)

        cls.page = UrbanRoutesPage(cls.driver)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

        #------Test Cases and Expected Outcomes -----
    def test_set_route(self):
        self.page.set_from("East 2nd Street, 601")
        self.page.set_to("1300 1st St")

        assert "East 2nd Street, 601" in self.driver.page_source
        assert "1300 1st St" in self.driver.page_source

        # ------Selecting the Supportive Plan -----
    def test_choose_supportive_taxi(self):
        self.page.set_from("East 2nd Street, 601")
        self.page.set_to("1300 1st St")

        self.page.click_call_taxi()
        self.page.choose_supportive()

        assert "Supportive" in self.driver.page_source

        # ------Filling in the Phone Number -----
    def test_fill_phone_number(self):
        self.page.set_from("East 2nd Street, 601")
        self.page.set_to("1300 1st St")

        self.page.click_call_taxi()
        self.page.choose_supportive()

        self.page.open_phone_modal()
        self.page.enter_phone(data.PHONE_NUMBER)

        sms_code = helpers.retrieve_phone_code(self.driver)
        self.page.enter_sms_code(sms_code)

        assert sms_code is not None

        # ------Fill in the Payment -----

    def test_fill_card(self):
        self.page.set_from("East 2nd Street, 601")
        self.page.set_to("1300 1st St")

        self.page.click_call_taxi()
        self.page.choose_supportive()

        # ---- CREDIT CARD STEP ----
        self.page.open_payment()
        self.page.click_add_card()
        self.page.fill_card(data.CARD_NUMBER, data.CARD_CODE)
        self.page.link_card()

        assert self.page.is_card_added()

    #-----Comment_for_driver-----
    def test_comment_for_driver(self):
        # 1) Set route
        self.page.set_from(data.ADDRESS_FROM)
        self.page.set_to(data.ADDRESS_TO)

        # 2) Call taxi + choose plan
        self.page.click_call_taxi()
        self.page.choose_supportive()

        # 3) Add comment for driver (NO payment here)
        self.page.add_comment_for_driver(data.MESSAGE_FOR_DRIVER)

        # 4) Verify comment entered (stable check)
        assert data.MESSAGE_FOR_DRIVER in self.driver.page_source

    #----- Blanket and Handkerchiefs------

    def test_order_blanket_and_handkerchiefs(self):
        # 1) Set route
        self.page.set_from(data.ADDRESS_FROM)
        self.page.set_to(data.ADDRESS_TO)

        # 2) Call taxi + choose plan
        self.page.click_call_taxi()
        self.page.choose_supportive()

        # 3) Add comment for driver (NO payment here)
        self.page.add_comment_for_driver(data.MESSAGE_FOR_DRIVER)

        # 4) order blanket and handkerchiefs
        self.page.select_blanket_and_handkerchiefs()
        assert True

    #------ Ordering 2 Ice Creams (Supportive Taxi)-------
    def test_order_2_ice_creams(self):
        # 1) Set route
        self.page.set_from(data.ADDRESS_FROM)
        self.page.set_to(data.ADDRESS_TO)

        # 2) Call taxi + choose plan
        self.page.click_call_taxi()
        self.page.choose_supportive()

        # 3) Comment (keep if your build needs it for extras section)
        self.page.add_comment_for_driver(data.MESSAGE_FOR_DRIVER)

        # 4) Add 2 ice creams
        assert self.page.add_ice_creams(2) is True

    # ---- Order Taxi + Car search modal ----
    def test_order_taxi(self):
        self.page.set_from(data.ADDRESS_FROM)
        self.page.set_to(data.ADDRESS_TO)
        self.page.click_call_taxi()
        self.page.choose_supportive()

        self.page.add_comment_for_driver(data.MESSAGE_FOR_DRIVER)

        # call it (no assert on return)
        self.page.select_blanket_and_handkerchiefs()

        assert self.page.add_ice_creams(2) is True
        assert self.page.order_taxi_and_assert_search_modal() is True

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()