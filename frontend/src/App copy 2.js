import './App.css';
import React, {useEffect, useState} from 'react';
import axios from 'axios';
import * as ReactBootStrap from 'react-bootstrap';

axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';

const App = () => {
  const [apiResponse, setApiResponse] = useState({
    match_table : '',
    f1_score : 0
  })
  const [loading, setLoading] = useState(false)

  const apiCall = async () => {
    try {
      axios.get('http://localhost:5000/predict').then(response => {
      setApiResponse({
        match_table : response.data.return,
        f1_score : response.data.F1_Score
      })
      setLoading(true);
      console.log(response)
    });
    } catch (e) {
      console.log(e);
    }
  };

  useEffect(() => {
    apiCall();
  }, []);
    // console.log(typeof(apiResponse.match_table))
    // console.log(apiResponse.match_table)

  return (
    <div>
      {loading ?     
        <div class="row">
        <div class="column">
          <table>
            <thead>
              <tr>
                {/* {apiResponse.match_table[0].map((item, index) => {
                  return <th>{item}</th>;
                })} */}
                <th>Player 1</th>
                <th>Player 2</th>
                <th>Match Result</th>
                <th>Predicted Result</th>
              </tr>
            </thead>
            <tbody>
              {apiResponse && apiResponse.match_table && apiResponse.match_table.slice(1, apiResponse.match_table.length).map((item, index) => {
                return (
                  <tr>
                    <td>{item[0]}</td>
                    <td>{item[1]}</td>
                    <td>{item[2]}</td>
                    <td>{item[3]}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div> 
        <div class='column'>
          <p>F1 Score: {apiResponse.f1_score}</p>
        </div>
      </div> 
      : <ReactBootStrap.Spinner animation="border" />}
    </div>




      // {/* <p>Hello : <div>
      //               {apiResponse.match_table && apiResponse.match_table.map((item, index) => { return( <div key={index+1}>{item.value}</div> ) } ) }
      //            </div></p> */}
      
      // {/* {apiResponse ? (
      //   <div>
      //     <p>API response: {apiResponse.f1_score}</p>
      //     <p>{ apiResponse.match_table.map((item, index) => { return( <div key={index+1}>{item.value}</div> ) } ) }</p>
      //   </div>
      // ) : (
      //   <p>Loading...</p>
      // )} */}



    // </div>
  );
}

export default App;
