import * as firebase from 'firebase'
import config from './config'
import React from 'react'
import { render } from 'react-dom'
import $ from 'jquery'
import App from './components/app'

class AppContainer {
  constructor(props) {

    // bootstrap the app
    firebase.initializeApp(config);

    // connect to services
    this.app = firebase.app();
    this.auth = firebase.auth();
    this.storage = firebase.storage();
    this.messaging = firebase.messaging();
    this.database = firebase.database();

    // handle auth changes
    this.auth.onAuthStateChanged(user => this.onAuthStateChanged);

    // firebase.database().ref('/path/to/ref').on('value', snapshot => );
    // firebase.messaging().requestPermission().then(() => { });
    // firebase.storage().ref('/path/to/ref').getDownloadURL().then(() => { });

    let appEl = document.getElementById('mainApp');

    // if we have an app
    if (appEl) {
      render(<App />, appEl)
    }

  }

}

$(() => {
  new AppContainer()
})