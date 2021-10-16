import React from "react";
import Map from "./components/Map";

class App extends React.Component {
  constructor(props) {
    super(props)
  }

  render() {
    return (
      <div class="App">
        <nav class="navbar navbar-dark bg-dark text-center">
          <div class="container-fluid justify-content-center navbar-brand">Arson Map</div>
        </nav>
        <div class="container">
          <Map/>          
        </div>
      </div>
    )
  }
}

export default App;
