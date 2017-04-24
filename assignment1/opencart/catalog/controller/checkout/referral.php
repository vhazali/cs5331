<?php
class ControllerCheckoutReferral extends Controller {
	public function index() {
		$this->language->load('checkout/checkout');

		$this->data['text_referral'] = $this->language->get('text_referral');
		$this->data['button_continue'] = $this->language->get('button_continue');

		if (isset($this->session->data['referral_id'])) {
			$this->data['referral_id'] = $this->session->data['referral_id'];
		} else {
			// 0 is default if no referrer
			$this->data['referral_id'] = 0;
		}

		if (file_exists(DIR_TEMPLATE . $this->config->get('config_template') . '/template/checkout/referral.tpl')) {
			$this->template = $this->config->get('config_template') . '/template/checkout/referral.tpl';
		} else {
			$this->template = 'default/template/checkout/referral.tpl';
		}

		$this->response->setOutput($this->render());
	}

	public function validate() {
		$this->language->load('checkout/checkout');

		$this->session->data['referral_id'] = 0;
		$json = array();
		if (isset($this->request->post['referral_id'])) {
			$referral_id = $this->request->post['referral_id'];
			
			if(!empty($referral_id)) {
				if (!is_numeric($referral_id)) {
					$json['error']['warning'] = $this->language->get('error_referral_numeric');
				} else {
					if (!is_int($referral_id + 0)) {
						$json['error']['warning'] = $this->language->get('error_referral');
					} else {
						if ($referral_id == 0) {
							//There is no referrer
							$this->session->data['referral_id'] = (int) $referral_id;
						} else {
							// check whether the referral id is a valid customer id
							$this->load->model('account/customer');
							$result = $this->model_account_customer->getCustomer($referral_id);
							if (count($result) == 0) {
								$json['error']['warning'] = $this->language->get('error_referral');
							} else {
								if ($this->customer->isLogged() && $this->customer->getId() == $referral_id) {
									$json['error']['warning'] = $this->language->get('error_referral');
								} else {
									$this->session->data['referral_id'] = (int) $referral_id;
								}
							}
						}
					}
				}
			}
		}
		$this->response->setOutput(json_encode($json));
	}
}
?> 