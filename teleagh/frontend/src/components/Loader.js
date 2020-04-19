import React from "react";
import styled from "styled-components";

const LoaderContainer  = styled.div`
  display: flex;
  
  .skele-column {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 0 auto;
    max-width: 500px;  
    flex-grow: 1;
  }
  
  .skele {
    display: inline-block;
    position: relative;
    overflow: hidden;
    background-color: #eee;
  
    &::after {
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      transform: translateX(-100%);
      background-image: linear-gradient(
        90deg,
        rgba(255, 255, 255, 0) 0,
        rgba(255, 255, 255, 0.2) 20%,
        rgba(255, 255, 255, 0.5) 60%,
        rgba(255, 255, 255, 0)
      );
      animation: shimmer 2s infinite;
      content: '';
    }
  
    @keyframes shimmer {
      100% {
        transform: translateX(100%);
      }
    }
  }
  
  .skele-title {
    margin: 2rem 0;
    width: 40%;
    height: 1rem;
  }
  
  .skele-header {
    margin-top: 1.5rem;
    width: 90%;
    height: 1rem;
  }
  
  .skele-content {
    margin-top: 1rem;
    width: 90%;
    height: 6rem;
  }
  
`;

function Loader({ desktopView }) {
  return (
    <LoaderContainer>
      {
        !desktopView ? (
          <div className="skele-column">
            <div className="skele skele-title"/>
            <div className="skele skele-header"/>
            <div className="skele skele-content"/>
            <div className="skele skele-header"/>
            <div className="skele skele-content"/>
          </div>
        ) : (
          <>
            <div className="skele-column">
              <div className="skele skele-title"/>
              <div className="skele skele-header"/>
              <div className="skele skele-content"/>
              <div className="skele skele-header"/>
              <div className="skele skele-content"/>
            </div>
            <div className="skele-column">
              <div className="skele skele-title"/>
              <div className="skele skele-header"/>
              <div className="skele skele-content"/>
              <div className="skele skele-header"/>
              <div className="skele skele-content"/>
            </div>
          </>
        )
      }
    </LoaderContainer>
  )
}

export default Loader;
