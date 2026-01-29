from selenium.webdriver.common.by import By
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException



import helpers

class UrbanRoutesPage:
    # ---------- Test Cases and Expected Outcomes ----------
    FROM_FIELD = (By.ID, "from")
    TO_FIELD = (By.ID, "to")

    CALL_TAXI_BUTTON = (By.XPATH, "//button[contains(text(),'Call a taxi')]")

    # ------Selecting the Supportive Plan -----
    SUPPORTIVE_TAXI = (By.XPATH, "//div[contains(text(),'Supportive')]")

    # A “selected” / active tariff label (best-effort generic)
    SELECTED_TARIFF_NAME = (
        By.XPATH,
        "//*[contains(@class,'active') or contains(@class,'selected')]//*[contains(.,'Supportive')]")

    # ------Filling in the Phone Number -----
    PHONE_INPUT = (By.ID, "phone")
    PHONE_LABEL = (By.CSS_SELECTOR, "label[for='phone']")
    SMS_CODE_INPUT = (By.ID, "code")
    CODE_LABEL = (By.CSS_SELECTOR, "label[for='code']")

    PHONE_BUTTON = (By.XPATH,"//*[contains(.,'Phone number') or contains(.,'Phone')][self::button or self::div or self::span]")
    PHONE_NEXT_BUTTON = (By.XPATH, "//button[contains(.,'Next') or contains(.,'Continue') or contains(.,'Confirm')]")
    SMS_CONFIRM_BUTTON = (By.XPATH, "//button[contains(.,'Confirm') or contains(.,'Submit')]")

    # ------Filling in payment  -----
    PAYMENT_METHOD_BUTTON = (By.XPATH,"//*[contains(.,'Payment method') or contains(.,'Payment') or contains(.,'Card')][self::button or self::div or self::span]")
    ADD_CARD_BUTTON = (By.XPATH, "//*[contains(.,'Add card') or contains(.,'Add a card')][self::button or self::div or self::span]")
    CARD_NUMBER_INPUT = (By.XPATH,"//input[@id='number' or contains(@placeholder,'Card number') or contains(@aria-label,'Card number')]")
    CARD_CODE_INPUT = (By.CSS_SELECTOR,"input#code.card-input, input#code, input[name='code'], input[placeholder*='CVV'], input[placeholder*='CVC']")
    LINK_CARD_BUTTON = (By.XPATH, "//button[contains(.,'Link')]")
    CARD_INPUTS = (By.CSS_SELECTOR, "input.card-input")
    # optional but helpful to assert card exists after linking
    CARD_ADDED_BADGE = (By.XPATH, "//*[contains(.,'Card')]")
    CARD_INPUTS = (By.CSS_SELECTOR, "input.card-input")
    CARD_NUMBER_INPUT = (By.CSS_SELECTOR, "input#number, input.card-input#number, input.card-input")
    CARD_CODE_INPUT = (By.CSS_SELECTOR, "input#code, input.card-input#code")

    # ---- Comment for driver ----
    COMMENT_INPUT = (By.CSS_SELECTOR, "textarea")
    COMMENT_SECTION_BUTTON = (By.XPATH,"//*[contains(.,'comment') or contains(.,'Comment') or contains(.,'driver') or contains(.,'Driver')][self::button or self::div or self::span]")
    COMMENT_FOR_DRIVER_INPUT = (By.ID, "comment")
    COMMENT_INPUT = (By.ID, "comment")
    COMMENT_LABEL = (By.CSS_SELECTOR, "label[for='comment']")

    # -----Ordering a Blanket and Handkerchiefs -----
    BLANKET_TOGGLE_INPUT = (By.CSS_SELECTOR, "input[name='blanket'], input#blanket")
    BLANKET_TOGGLE_LABEL = (By.CSS_SELECTOR, "label[for='blanket'], label[for='blanket-and-handkerchiefs']")
    BLANKET_TOGGLE_CONTAINER = (By.XPATH,"//*[contains(.,'Blanket') and contains(.,'handker')]/ancestor::*[self::div or self::label][1]")
    BLANKET_ROW = (By.XPATH,"//*[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'blanket') "
        "and contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'handker')]"
        "/ancestor::*[self::div or self::label][1]")
    BLANKET_CHECKBOX = (By.XPATH, "(.//*//input[@type='checkbox'])[1]")

    # ----- Ordering 2 Ice Creams (Supportive Taxi) -----
    ICE_CREAM_COUNTER_VALUE = (By.CSS_SELECTOR, "div.counter-value")  # fallback if there are multiple counters
    ICE_CREAM_PLUS_GENERIC = (By.XPATH, "//button[contains(., '+')]")  # fallback
    ICE_CREAM_PLUS = (By.XPATH,"//*[contains(., 'Ice cream') or contains(., 'Ice Cream')]/ancestor::div[1]//button[contains(., '+')]")
    ICE_CREAM_MINUS = (By.XPATH,"//*[contains(., 'Ice cream') or contains(., 'Ice Cream')]/ancestor::div[1]//button[contains(., '-')]")
    ICE_CREAM_VALUE_IN_BLOCK = (By.XPATH,"//*[contains(., 'Ice cream') or contains(., 'Ice Cream')]/ancestor::div[1]//*[contains(@class,'counter') or contains(@class,'value') or self::div]")
    # A “section anchor” so we can scroll to the extras area reliably
    EXTRAS_ANCHOR = (By.XPATH, "//*[contains(.,'Blanket') or contains(.,'Handkerchief') or contains(.,'Ice')]")
    # Try to find the Ice Cream row/block (text can vary a little)
    ICE_CREAM_BLOCK = (By.XPATH,"//*[contains(translate(., 'ICECREAM', 'icecream'), 'ice') and contains(translate(., 'ICECREAM', 'icecream'), 'cream')]/ancestor::*[self::div or self::li][1]")
    # Candidate “plus” locators (different builds use different markup)
    ICE_CREAM_PLUS_IN_BLOCK = (By.XPATH,"//*[contains(translate(., 'ICECREAM', 'icecream'), 'ice') and contains(translate(., 'ICECREAM', 'icecream'), 'cream')]/ancestor::*[self::div or self::li][1]//*[self::button or self::div][.='+' or contains(@class,'plus') or contains(@aria-label,'plus') or contains(@data-testid,'plus')]")
    PLUS_ANYWHERE = (By.XPATH,"//*[self::button or self::div][.='+' or contains(@class,'plus') or contains(@aria-label,'plus') or contains(@data-testid,'plus')]")

    # ---- Order Taxi + Car search modal ----
    ORDER_TAXI_BUTTON = (By.XPATH, "//button[contains(.,'Order')]")
    CAR_SEARCH_MODAL = (By.XPATH,"//*[contains(., 'Searching') or contains(., 'searching') or contains(., 'car') or contains(., 'Car')]")
    ORDER_TAXI_BUTTON = (By.XPATH,"//button[contains(.,'Order') or contains(.,'Book') or contains(.,'Taxi')]")
    ORDER_BUTTON = (By.XPATH, "//button[contains(text(),'Order')]")
    # --- Order Taxi ---
    ORDER_TAXI_BUTTON_PRIMARY = (By.XPATH, "//button[contains(.,'Order')]")
    ORDER_TAXI_BUTTON_FALLBACK = (By.XPATH,"//button[contains(.,'Book') or contains(.,'Submit') or contains(.,'Confirm')]")
    # Modal (also make flexible)
    CAR_SEARCH_MODAL = (By.XPATH,"//*[contains(.,'Searching') or contains(.,'searching') or contains(.,'Looking for') or contains(.,'car')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ---------- Test Cases and Expected Outcomes ----------
    def set_from(self, text):
        field = self.wait.until(EC.element_to_be_clickable(self.FROM_FIELD))
        field.clear()
        field.send_keys(text)

    def set_to(self, text):
        field = self.wait.until(EC.element_to_be_clickable(self.TO_FIELD))
        field.clear()
        field.send_keys(text)

    def click_call_taxi(self):
        self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON)).click()

    # ------Selecting the Supportive Plan -----
    def choose_supportive(self):
        self.wait.until(EC.element_to_be_clickable(self.SUPPORTIVE_TAXI)).click()

    # ------Filling in the Phone Number -----
    def open_phone_modal(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.PHONE_BUTTON))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        self.driver.execute_script("arguments[0].click();", btn)

        # IMPORTANT: wait for the phone input to actually appear
        self.wait.until(EC.presence_of_element_located(self.PHONE_INPUT))

    def enter_phone(self, phone):
        # Wait until phone input exists/visible
        field = self.wait.until(EC.visibility_of_element_located(self.PHONE_INPUT))

        # Sometimes label is missing or covered -> don't hard fail on it
        try:
            lbl = self.driver.find_elements(*self.PHONE_LABEL)
            if lbl:
                self.wait.until(EC.element_to_be_clickable(self.PHONE_LABEL)).click()
        except Exception:
            pass

        # Click input directly (more reliable than label)
        try:
            field.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", field)

        field.clear()
        field.send_keys(phone)

        # Click Next/Continue (your existing code is fine; keep it)
        btn = self.wait.until(EC.presence_of_element_located(self.PHONE_NEXT_BUTTON))
        self.wait.until(lambda d: btn.is_displayed() and btn.is_enabled())
        self.driver.execute_script("arguments[0].click();", btn)

    def enter_sms_code(self, code):
        self.wait.until(EC.element_to_be_clickable(self.CODE_LABEL)).click()

        code_field = self.wait.until(
            EC.visibility_of_element_located(self.SMS_CODE_INPUT))
        code_field.clear()
        code_field.send_keys(code)

        self.wait.until(EC.element_to_be_clickable(self.SMS_CONFIRM_BUTTON)).click()

    # ------Fill in the Payment -----

    def _scroll_center(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)

    def _js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def _switch_to_frame_with(self, locator, timeout=2):
        """
        Some builds render card inputs inside an iframe. This tries each iframe and
        switches into the one that contains `locator`.
        """
        self.driver.switch_to.default_content()
        frames = self.driver.find_elements(By.TAG_NAME, "iframe")
        for frame in frames:
            try:
                self.driver.switch_to.frame(frame)
                WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
                return True
            except Exception:
                self.driver.switch_to.default_content()
        return False

    def open_payment(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.PAYMENT_METHOD_BUTTON))
        self._scroll_center(btn)
        self._js_click(btn)
        self.wait.until(EC.presence_of_element_located(self.ADD_CARD_BUTTON))

    def click_add_card(self):
        add = self.wait.until(EC.element_to_be_clickable(self.ADD_CARD_BUTTON))
        self._scroll_center(add)
        self._js_click(add)

        # card form may be in iframe or main DOM
        if not self._switch_to_frame_with(self.CARD_NUMBER_INPUT):
            self.driver.switch_to.default_content()

        self.wait.until(EC.visibility_of_element_located(self.CARD_NUMBER_INPUT))

    def fill_card(self, number: str, code: str):
        # try to get into the iframe that contains card inputs
        if not self._switch_to_frame_with(self.CARD_NUMBER_INPUT):
            self.driver.switch_to.default_content()

        # card number
        number_input = self.wait.until(EC.presence_of_element_located(self.CARD_NUMBER_INPUT))
        self.driver.execute_script("arguments[0].click();", number_input)
        number_input.clear()
        number_input.send_keys(number)

        # trigger the next field (CVV) to render
        number_input.send_keys(Keys.TAB)

        # 1) try CVV by id=code (but using PRESENCE not VISIBILITY)
        code_input = None
        try:
            code_input = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.CARD_CODE_INPUT)
            )
        except Exception:
            pass

        # 2) fallback: CVV is often the 2nd input.card-input
        # 2) try CVV by id=code first (presence)
        code_input = None
        try:
            code_input = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.CARD_CODE_INPUT)
            )
        except Exception:
            pass

        # fallback: pick the *displayed* CVV among card-inputs
        if code_input is None or (hasattr(code_input, "is_displayed") and not code_input.is_displayed()):
            inputs = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(self.CARD_INPUTS)
            )
            # pick the first displayed input that is NOT the number input
            displayed = [el for el in inputs if el.is_displayed()]
            if len(displayed) < 2:
                # if only one is displayed, use the last element anyway
                code_input = inputs[-1]
            else:
                code_input = displayed[1]

        # click via JS (more reliable)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", code_input)
        self.driver.execute_script("arguments[0].focus();", code_input)
        self.driver.execute_script("arguments[0].click();", code_input)

        # IMPORTANT: don't use clear() — it often throws "not interactable" on this field
        code_input.send_keys(Keys.COMMAND, "a")
        code_input.send_keys(Keys.BACKSPACE)
        code_input.send_keys(code)

        # blur so Link enables
        code_input.send_keys(Keys.TAB)

        # Link button is outside iframe
        self.driver.switch_to.default_content()

    def link_card(self):
        link = self.wait.until(EC.element_to_be_clickable(self.LINK_CARD_BUTTON))
        self._scroll_center(link)
        self._js_click(link)

    def is_card_added(self):
        # simple “something card-related exists” check
        return len(self.driver.find_elements(*self.CARD_ADDED_BADGE)) > 0

    # ---- Comment for driver ----
    def add_comment_for_driver(self, comment: str):
        # always return to main page context
        self.driver.switch_to.default_content()

        # wait until the comment input exists
        field = self.wait.until(EC.presence_of_element_located(self.COMMENT_INPUT))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", field)

        # If label is blocking clicks, click the label instead (it focuses the input)
        try:
            label = self.driver.find_element(*self.COMMENT_LABEL)
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", label)
            try:
                label.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", label)
        except Exception:
            # fallback: focus input via JS (avoids intercepted click)
            self.driver.execute_script("arguments[0].focus();", field)

        # clear + type (clear() can fail sometimes on some inputs; use Ctrl/Cmd+A + Backspace)
        try:
            field.clear()
        except Exception:
            field.send_keys(Keys.COMMAND, "a")
            field.send_keys(Keys.BACKSPACE)

        field.send_keys(comment)

        # verify entered
        assert field.get_attribute("value") == comment

    # ----- Blanket and Handkerchiefs------
    def select_blanket_and_handkerchiefs(self):
        """
        Turns ON Blanket & Handkerchiefs.
        Does not touch route/plan/phone/card/comment.
        """

        self.driver.switch_to.default_content()

        # 1) Find the row by text, then the checkbox inside it
        row = self.wait.until(EC.presence_of_element_located(self.BLANKET_ROW))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", row)

        checkbox = row.find_element(*self.BLANKET_CHECKBOX)

        # 2) If it's already ON, do nothing
        try:
            if checkbox.is_selected():
                return
        except Exception:
            pass

        # 3) Click the ROW (more reliable than clicking checkbox directly)
        try:
            row.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", row)

        # 4) Re-grab checkbox (DOM can re-render) + verify it turned ON
        row = self.wait.until(EC.presence_of_element_located(self.BLANKET_ROW))
        checkbox = row.find_element(*self.BLANKET_CHECKBOX)

        self.wait.until(lambda d: checkbox.is_selected())

        return True

    #------ Ordering 2 Ice Creams (Supportive Taxi)-------
    def _safe_js_click(self, el):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        try:
            el.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", el)

    def get_ice_cream_count(self) -> int:
        """
        Best-effort: read the ice cream counter number.
        """
        self.driver.switch_to.default_content()

        # Try to find the number inside the ice cream block
        try:
            block = self.wait.until(EC.presence_of_element_located(self.ICE_CREAM_BLOCK))
            text = block.text
            # find first integer in the block text
            import re
            nums = re.findall(r"\b\d+\b", text)
            if nums:
                return int(nums[-1])
        except Exception:
            pass

        # Fallback: if your build uses multiple counters, this may be noisy,
        # but it’s better than failing to read anything.
        try:
            values = self.driver.find_elements(*self.ICE_CREAM_COUNTER_VALUE)
            for v in values:
                t = (v.text or "").strip()
                if t.isdigit():
                    return int(t)
        except Exception:
            pass

        return -1  # couldn't read

    def add_ice_creams(self, qty: int = 2) -> bool:
        """
        Click '+' qty times for Ice Creams.
        Does NOT touch route/plan/phone/card/comment.
        """

        self.driver.switch_to.default_content()

        # 1) Scroll down to extras area so elements render
        try:
            anchor = self.wait.until(EC.presence_of_element_located(self.EXTRAS_ANCHOR))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", anchor)
        except Exception:
            # hard fallback: scroll lower on page
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 2) Find a usable "+" element
        def find_plus():
            # Best: "+" inside the Ice Cream block
            try:
                els = self.driver.find_elements(*self.ICE_CREAM_PLUS_IN_BLOCK)
                for el in els:
                    if el.is_displayed():
                        return el
            except Exception:
                pass

            # Fallback: any visible "+" on screen (often only ice cream has +)
            els = self.driver.find_elements(*self.PLUS_ANYWHERE)
            for el in els:
                try:
                    if el.is_displayed():
                        return el
                except Exception:
                    continue
            return None

        # 3) Click it qty times (use JS click to avoid intercept issues)
        for _ in range(qty):
            plus = None
            self.wait.until(lambda d: find_plus() is not None)
            plus = find_plus()

            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", plus)
            try:
                plus.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", plus)

        return True

    # ---- Order Taxi + Car search modal ----
    def order_taxi_and_assert_search_modal(self) -> bool:
        self.driver.switch_to.default_content()

        # scroll down so footer buttons load / become visible
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # find Order button using multiple locators
        order_btn = None
        for loc in (self.ORDER_TAXI_BUTTON_PRIMARY, self.ORDER_TAXI_BUTTON_FALLBACK):
            try:
                order_btn = WebDriverWait(self.driver, 4).until(EC.presence_of_element_located(loc))
                break
            except Exception:
                pass

        if order_btn is None:
            raise Exception("Order button not found (likely prerequisites not completed OR locator mismatch).")

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", order_btn)
        try:
            WebDriverWait(self.driver, 4).until(
                EC.element_to_be_clickable((order_btn.tag_name, order_btn.get_attribute("xpath"))))
        except Exception:
            pass

        try:
            order_btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", order_btn)

        # modal appears
        modal = self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_MODAL))
        assert modal.is_displayed()
        return True



