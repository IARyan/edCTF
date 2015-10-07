import Ember from 'ember';

export default Ember.Component.extend({
  isShowingLoginModal: false,
  isShowingRegisterModal: false,
  actions: {
    toggleLoginModal: function() {
      this.toggleProperty('isShowingLoginModal');
    },
    toggleRegisterModal: function() {
      this.toggleProperty('isShowingRegisterModal');
    },
  }
});
