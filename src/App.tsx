import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { LinkContainer } from "react-router-bootstrap";

import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import NavbarCollapse from "react-bootstrap/NavbarCollapse";
import Container from "react-bootstrap/Container";

import Properties from "./Components/Properties/Properties";
import Home from "./Components/Home/Home";
import "./App.css";

function App(): React.ReactElement {
  const [output, setOutput] = useState(0);

  useEffect(() => {
    fetch("/api/v1/properties?search_query=DOMB ALLAN&search_type=owner")
      .then((res) => res.json())
      .then((data) => {
        setOutput(data.results[0].location);
      });
  }, []);

  const renderRouter = () => (
    <Router>
      <div>
        <Navbar bg="dark" variant="dark" expand="lg" fixed="top">
          <LinkContainer to="/">
            <Navbar.Brand className="navText">PHL Tenant Tools</Navbar.Brand>
          </LinkContainer>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <NavbarCollapse>
            <Nav className="mr-auto">
              <LinkContainer to="/" className="navText">
                <Nav.Link>Home</Nav.Link>
              </LinkContainer>
              <LinkContainer to="/properties" className="navText">
                <Nav.Link>Properties</Nav.Link>
              </LinkContainer>
            </Nav>
          </NavbarCollapse>
        </Navbar>
        <Container style={{ marginTop: "5vw" }}>
          <Switch>
            <Route path="/properties">
              <Properties />
            </Route>
            <Route path="/">
              <Home />
            </Route>
          </Switch>
        </Container>
      </div>
    </Router>
  );

  return (
    <div className="App">
      {renderRouter()}
      <p>The API output is {output}.</p>
    </div>
  );
}

export default App;
