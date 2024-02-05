import { useRef, useState } from 'react';
import './App.css';
import { calculateExpression, downloadAllCalculations } from './api';

const App = () => {
  const [expression, setExpression] = useState("");

  const isOperator = c => {
    return c === "+" || c === "-" || c === "*" || c === "/" ? true : false;
  };

  const handleDigitClick = str => {
    if (expression.length && isOperator(expression[expression.length - 1])) str = " " + str;
    setExpression(expression + str);
  };

  const handleOperatorClick = str => {
    if (expression.length) str = " " + str;
    setExpression(expression + str);
  };

  const handleSpaceClick = e => {
    setExpression(expression + " ");
  };

  const handleDelClick = e => {
    if (expression.length) {
      setExpression(expression.slice(0, -1).trimEnd());
    }
  };

  const handleResetClick = () => {
    setExpression("");
  };

  const handleEnterClick = async e => {
    try {
      const res = await calculateExpression(expression);
      setExpression(res.data.result);
      console.log(res);
    } catch (err) {
      if (err?.response?.status === 400) setExpression("Invalid expression");
      else setExpression("Server error");
    }
  };

  const handleDownloadClick = async () => {
    try {
      const res = await downloadAllCalculations();

      // create file link in browser's memory
      const href = URL.createObjectURL(res.data);

      // create "a" HTML element with href to file & click
      const link = document.createElement('a');
      link.href = href;
      link.setAttribute('download', 'calculations.csv'); //or any other extension
      document.body.appendChild(link);
      link.click();

      // clean up "a" element & remove ObjectURL
      document.body.removeChild(link);
      URL.revokeObjectURL(href);
    } catch (err) {
      console.log(err);
    }
  }

  return (
    <div className='app'>
      <div className='title'>NPI Calculator</div>
      <div className='calculator-container'>
        <input
          onKeyDown={e => {
            if (e.key === "Enter") handleEnterClick();
          }}
          className='calculator-input'
          value={expression}
          onChange={e => setExpression(e.target.value)}
        />
        <div className='calculator-buttons-container'>
          <button className='calculator-button' onClick={handleSpaceClick}>SPACE</button>
          <button className='calculator-button' onClick={handleDelClick}>DEL</button>
          <button className='calculator-button' onClick={handleResetClick}>RESET</button>
          <button className='calculator-button' onClick={handleEnterClick}>ENTER</button>
          <button className='calculator-button' onClick={e => handleDigitClick('.')}>.</button>
          <button className='calculator-button' onClick={e => handleDigitClick('0')}>0</button>
          <button className='calculator-button' onClick={e => handleDigitClick('1')}>1</button>
          <button className='calculator-button' onClick={e => handleDigitClick('2')}>2</button>
          <button className='calculator-button' onClick={e => handleDigitClick('3')}>3</button>
          <button className='calculator-button' onClick={e => handleDigitClick('4')}>4</button>
          <button className='calculator-button' onClick={e => handleDigitClick('5')}>5</button>
          <button className='calculator-button' onClick={e => handleDigitClick('6')}>6</button>
          <button className='calculator-button' onClick={e => handleDigitClick('7')}>7</button>
          <button className='calculator-button' onClick={e => handleDigitClick('8')}>8</button>
          <button className='calculator-button' onClick={e => handleDigitClick('9')}>9</button>
          <button className='calculator-button'></button>
          <button className='calculator-button' onClick={e => handleOperatorClick('+')}>+</button>
          <button className='calculator-button' onClick={e => handleOperatorClick('-')}>-</button>
          <button className='calculator-button' onClick={e => handleOperatorClick('*')}>*</button>
          <button className='calculator-button' onClick={e => handleOperatorClick('/')}>/</button>
        </div>
      </div>
      <button className='download-button' onClick={e => handleDownloadClick()}>Download every calculation we've made so far</button>
    </div>
  );
};

export default App;
