Vue.http.headers.common['X-CSRFToken'] = "{{ csrf_token }}";
new Vue({
  el: '#starting',
  delimiters: ['${', '}'],
  data: {
    products: [],
    cartItems: [],
    checkoutErrors: [],
    orders: [],
    promo_codes: [],
    email: '',
    loading: true,
    cart: {},
    currentProduct: {},
    search_term: '',
  },
  mounted: function () {
    this.getProducts();
    this.getCart();
  },
  methods: {
    getProducts: function () {
      let api_url = '/products/';
      if (this.search_term !== '' || this.search_term !== null) {
        api_url = `/products/?search=${this.search_term}`;
      }
      this.loading = true;
      this.$http.get(api_url)
        .then((response) => {
          this.products = response.data;
          this.loading = false;
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        })
    },
    getCart: function () {
      let sesionId = this.$cookies.get('sesionId');
      if (sesionId == null) {
        this.createCart();
      } else {
        this.loading = true;
        this.$http.get(`/carts/${sesionId}/`)
          .then((response) => {
            this.cart = response.data;
            this.getCartItems(this.cart.id);
            this.loading = false;
          })
          .catch((err) => {
            this.loading = false;
            this.$cookies.remove('sesionId');
            this.getCart();
            console.log(err);
          })
      }
    },
    getCartItems: function (sesionId) {
      this.loading = true;
      this.$http.get(`/carts/${sesionId}/items/`)
        .then((response) => {
          this.cartItems = response.data;
          this.loading = false;
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        })
    },
    createCart: function () {
      this.loading = true;
      this.$http.post(`/carts/`)
        .then((response) => {
          this.cart = response.data;
          this.$cookies.set('sesionId', this.cart.id);
          this.getCartItems(this.cart.id);
          this.loading = false;
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        })
    },
    clearCheckoutModal: function () {
      this.checkoutErrors = [];
      this.email = '';
    },
    checkoutCart: function () {
      this.loading = true;
      this.$http.post(`/carts/${this.cart.id}/checkout/`, { email: this.email })
        .then((response) => {
          this.order = response.data;
          this.$cookies.remove('sesionId');
          this.getCart();
          $('#checkoutModal').modal('hide');
          this.clearCheckoutModal();
        })
        .catch((err) => {
          this.loading = false;
          if (err.status == 400) {
            this.checkoutErrors = err.data.email;
          }
          console.log(err);
        })
    },
    deleteCartItem: function (id) {
      this.loading = true;
      this.$http.delete(`/carts/${this.cart.id}/items/${id}/`)
        .then((response) => {
          this.loading = false;
          this.getCart()
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        })
    },
    addCartItem: function (productId) {
      this.loading = true;
      this.$http.post(`/carts/${this.cart.id}/items/`, { product: productId })
        .then((response) => {
          this.getCart()
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        })
    },
    quantityChange: function (item) {
      this.loading = true;
      this.$http.put(`/carts/${this.cart.id}/items/${item.id}/`, item)
        .then((response) => {
          this.loading = false;
          this.getCart();
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        })
    },
    applyPromoCode: function () {
      this.loading = true;
      this.$http.patch(`/carts/${this.cart.id}/`, { promo_code: this.cart.promo_code })
        .then((response) => {
          this.loading = false;
          this.getCart();
        })
        .catch((err) => {
          this.cart.promo_code = '',
            this.loading = false;
          console.log(err);
        })
    },
    getOrders: function () {
      this.loading = true;
      this.$http.get(`/orders/`)
        .then((response) => {
          this.orders = response.data;
          this.loading = false;
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        })
    },
    getPromoCodes: function () {
      this.loading = true;
      this.$http.get(`/promocodes/`)
        .then((response) => {
          this.promo_codes = response.data;
          this.loading = false;
        })
        .catch((err) => {
          this.loading = false;
          console.log(err);
        })
    },
    checkoutIsDisabled: function () {
      if (this.email == '' || this.cartItems.length == 0)
        return true;
      return false;
    },
    showProductSescription: function (product) {
      this.currentProduct = product;
      $("#productDescriptionModal").modal('show');
    }
  }
});
