import Ember from 'ember';

export default Ember.Controller.extend({
  applicationController: Ember.inject.controller('application'),
  isShowingChallengeModal: false,
  actions: {
    login: function(authenticationData) {
      // Pass the authentication data up
      this.sendAction('login', authenticationData);
    },
    openLoginModal: function() {
      this.get('applicationController').set('isShowingLoginModal', true);
    },
    openChallenge: function(challenge_id) {
        this.set('challenge', this.store.find('challenge', challenge_id));
        this.set('isShowingChallengeModal', true);
    },
  }
});
