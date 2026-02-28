import React from 'react';
import './leftList.css';
import { useAuth0 } from '@auth0/auth0-react';

function LeftList({ potholes }){
    const {
        isLoading, // Loading state, the SDK needs to reach Auth0 on load
        isAuthenticated,
        error,
        loginWithRedirect: login, // Starts the login flow
        logout: auth0Logout, // Starts the logout flow
        user, // User profile
      } = useAuth0();
    
      const signup = () =>
        login({ authorizationParams: { screen_hint: "signup" } });
    
      const logout = () =>
        auth0Logout({ logoutParams: { returnTo: window.location.origin } });

    return(
        <div className="leftList">
            <div className="icon">
                <h1>PUPIL</h1>
            </div>

            <div className="potholes">
                <h2>Potholes</h2>

                    {/* Map out potholes id from arg */}

            </div>

            {/* {
                isAuthenticated ? (
                    <>
                        camera portal
                    </>
                ) : (
                    <>
                        <h2>Set Up Your Camera</h2>
                        <button onClick={signup}>Sign Up</button>
                        <button onClick={login}>Login</button>
                    </>
                )
            } */}

        </div>
    );
}

export default LeftList;