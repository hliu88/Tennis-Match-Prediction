import './App.css';
import React, {useEffect, useState} from 'react';
import axios from 'axios';
import styled from "styled-components";
import * as ReactBootStrap from 'react-bootstrap';

axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';

const types = ["Test", "Yesterday", "Today", "Tomorrow"];

const theme = {
  blue: {
    default: "#3f51b5",
    hover: "#283593"
  },
  pink: {
    default: "#e91e63",
    hover: "#ad1457"
  }
};

const Tab = styled.button`
  padding: 10px 40px;
  cursor: pointer;
  opacity: 0.6;
  background: white;
  border: 0;
  outline: 0;
  border-bottom: 2px solid transparent;
  transition: ease border-bottom 250ms;
  ${({ active }) =>
    active &&
    `
    border-bottom: 2px solid black;
    opacity: 1;
  `}
`;

const Button = styled.button`
  background-color: ${(props) => theme[props.theme].default};
  color: white;
  padding: 5px 15px;
  border-radius: 5px;
  outline: 0;
  text-transform: uppercase;
  margin: 10px 0px;
  cursor: pointer;
  box-shadow: 0px 2px 2px lightgray;
  transition: ease background-color 250ms;
  &:hover {
    background-color: ${(props) => theme[props.theme].hover};
  }
  &:disabled {
    cursor: default;
    opacity: 0.7;
  }
`;

const App = () => {
  const [apiResponse, setApiResponse] = useState({
    match_table : '',
    f1_score : 0
  })

  const [test, setTest] = useState({
    match_table : '',
    f1_score : 0,
    loaded: false,
    code : 0,
    notavail: false
  })

  const [today, setToday] = useState({
    match_table : '',
    f1_score : 0,
    loaded: false,
    code : 0,
    notavail: false
  })

  const [tomorrow, setTomorrow] = useState({
    match_table : '',
    f1_score : 0,
    loaded: false,
    code : 0,
    notavail: false
  })

  const [yesterday, setYesterday] = useState({
    match_table : '',
    f1_score : 0,
    loaded: false,
    code : 0,
    notavail: false
  })

  const apiCallTest = async () => {
    try {
      axios.get('http://localhost:5000/predict/test').then(response => {
      setTest({
        match_table : response.data.message,
        f1_score : response.data.F1_Score,
        loaded: true,
        code : response.status,
        notavail: false
      })
      if(response.data.message === 'NA'){
        setTest({
          notavail: true
        })
      }
    });
    } catch (e) {
      console.log(e);
    }
  };

  const apiCallToday = async () => {
    try {
      axios.get('http://localhost:5000/predict/today').then(response => {
      setToday({
        match_table : response.data.message,
        f1_score : response.data.F1_Score,
        loaded: true,
        code : response.status,
        notavail: false
      })
      if(response.data.message === 'NA'){
        setToday({
          notavail: true
        })
      }
    });
    } catch (e) {
      console.log(e);
      setToday({
        notavail: true
      })
    }
  };

  const apiCallYesterday = async () => {
    try {
      axios.get('http://localhost:5000/predict/yesterday').then(response => {
      setYesterday({
        match_table : response.data.message,
        f1_score : response.data.F1_Score,
        loaded: true,
        code : response.status,
        notavail: false
      })
      if(response.data.message === 'NA'){
        setYesterday({
          notavail: true
        })
      }
    });
    } catch (e) {
      console.log(e);
    }
  };

  const apiCallTomorrow = async () => {
    try {
      axios.get('http://localhost:5000/predict/tomorrow').then(response => {
      setTomorrow({
        match_table : response.data.message,
        f1_score : response.data.F1_Score,
        loaded: true,
        code : response.status,
        notavail: false
      })
      if(response.data.message === 'NA'){
        setTomorrow({
          notavail: true
        })
      }
    });
    } catch (e) {
      console.log(e);
    }
  };

  useEffect(() => {
    if(test.loaded == false){
      apiCallTest();
    }
    if(yesterday.loaded == false){
      apiCallYesterday();
    }
    if(today.loaded == false){
      apiCallToday();
    }
    if(tomorrow.loaded == false){
      apiCallTomorrow();
    }
    // apiCallYesterday();
    // apiCallToday();
    // apiCallTomorrow();
  }, []);

  // useEffect(() => {
  //   apiCallToday();
  //   console.log(today)
  // }, []);

  // useEffect(() => {
  //   apiCallTomorrow();
  // }, []);

  // useEffect(() => {
  //   apiCallYesterday();
  // }, []);
  
  function Table(props) {
    return (
      <div class="column">
        <table>
          <thead>
            <tr>
              <th>Player 1</th>
              <th>Player 2</th>
              <th>Match Result</th>
              <th>Predicted Result</th>
            </tr>
          </thead>
          <tbody>
            {props.notavail ?  <div class="column"><p>No Matches Available</p></div>:
            (props && props.match_table && props.match_table.slice(1, props.match_table.length).map((item, index) => {
              return (
                <tr>
                  <td>{item[0]}</td>
                  <td>{item[1]}</td>
                  <td>{item[2]}</td>
                  <td>{item[3]}</td>
                </tr>
              );
            })) 
          }
          </tbody>
        </table>
      </div>
    );
  }

  function TabGroup() {
    const [active, setActive] = useState(types[0]);
    return (
      <>
        <div>
          {types.map((type) => (
            <Tab
              forceRenderTabPanel={true}
              key={type}
              active={active === type}
              onClick={() => {
                setActive(type)
              }}
            >
              {type}
            </Tab>
          ))}
          {(() => {
            switch (active) {
              case "Test":   return test.notavail ? <p>No Matches Available</p> : test.loaded ? Table(test) : <ReactBootStrap.Spinner animation="border" />;
              case "Yesterday": return yesterday.notavail ? <p>No Matches Available</p> : yesterday.loaded ? Table(yesterday) : <ReactBootStrap.Spinner animation="border" />;
              case "Today":  return today.notavail ? <p>No Matches Available</p> : today.loaded ? Table(today) : <ReactBootStrap.Spinner animation="border" />;
              case "Tomorrow":  return tomorrow.notavail ? <p>No Matches Available</p> : tomorrow.loaded ? Table(tomorrow): <ReactBootStrap.Spinner animation="border" />;
            }
          })()}
        </div>
          
      </>
    );
  }

  return (
    <div>
      <TabGroup />  
    </div>
  );
}

export default App;
