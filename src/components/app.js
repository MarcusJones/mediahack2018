import React, { Component } from 'react'
import firebase from 'firebase'

export default class App extends Component {
  constructor(props) {
    super(props)

    this.state = {
      currentUser: null
    }
  }

  render() {
    return (
      <div>This is the app</div>
    )
  }
}