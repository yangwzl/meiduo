var vm = new Vue({
	el: '#app',
	data: {
		error_name: false,
		error_password: false,
		error_check_password: false,
		error_phone: false,
		error_allow: false,
		error_image_code: false,
		error_sms_code: false,

		username: '',
		password: '',
		password2: '',
		mobile: '',
		image_code:'',
		image_code_id: '',
		image_code_url: '',
		sms_send :'获取短信验证码',
		sms_code: '',
		allow: false,
		sending_flag:false,
	},
	mounted:function(){
		this.get_image_code()
	},
	methods: {
		get_image_code:function(){
			this.image_code_id = this.generate_uuid()
			this.image_code_url = "http://127.0.0.1:8000/image_codes/"+this.image_code_id
		},
		// #生成uuid
		generate_uuid: function(){
			var d = new Date().getTime();
			if(window.performance && typeof window.performance.now === "function"){
				d += performance.now(); //use high-precision timer if available
			}
			var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
				var r = (d + Math.random()*16)%16 | 0;
				d = Math.floor(d/16);
				return (c =='x' ? r : (r&0x3|0x8)).toString(16);
			});
			return uuid;
		},
		//获取短信验证码
		get_sms_code:function(){
			this.check_phone()
			this.check_image_code()
			if (this.error_phone == true || this.error_image_code == true){
				return
			}

			this.sms_code_url = "http://127.0.0.1:8000/sms_codes/" + this.mobile +"/?text=" + this.image_code + "&image_code_id=" + this.image_code_id
			axios.post(this.sms_code_url).then(response =>{
				var num = 60
				var t = setInterval(()=>{
					if (num == 1){
						this.sending_flag = true
					}else {
						num --
						this.sms_send = num+'秒'
						this.sending_flag = false
					}
				},1000,60)

			})

		},


		check_username: function (){
			var len = this.username.length;
			if(len<5||len>20) {
				this.error_name = true;
			} else {
				this.error_name = false;
			}
		},
		check_pwd: function (){
			var len = this.password.length;
			if(len<8||len>20){
				this.error_password = true;
			} else {
				this.error_password = false;
			}		
		},
		check_cpwd: function (){
			if(this.password!=this.password2) {
				this.error_check_password = true;
			} else {
				this.error_check_password = false;
			}		
		},
		check_phone: function (){
			var re = /^1[345789]\d{9}$/;
			if(re.test(this.mobile)) {
				this.error_phone = false;
			} else {
				this.error_phone = true;
			}
		},
		check_image_code: function (){
			if(!this.image_code) {
				this.error_image_code = true;
			} else {
				this.error_image_code = false;
			}	
		},
		check_sms_code: function(){
			if(!this.sms_code){
				this.error_sms_code = true;
			} else {
				this.error_sms_code = false;
			}
		},
		check_allow: function(){
			if(!this.allow) {
				this.error_allow = true;
			} else {
				this.error_allow = false;
			}
		},
		// 注册
		on_submit: function(){
			this.check_username();
			this.check_pwd();
			this.check_cpwd();
			this.check_phone();
			this.check_sms_code();
			this.check_allow();
		}
	}
});
