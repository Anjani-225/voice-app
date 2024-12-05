import React, { useState } from 'react';
import './Profile.css';  // For styling

const Profile = () => {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState('');

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();
        
        const userData = {
            first_name: firstName,
            last_name: lastName,
            password: password
        };

        // Send data to backend
        try {
            const response = await fetch('http://127.0.0.1:5000/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            });
            const result = await response.json();
            if (response.ok) {
                setMessage("User signed up successfully!");
                setMessageType("success");
            } else {
                setMessage(result.error || "Something went wrong.");
                setMessageType("error");
            }
        } catch (error) {
            setMessage("An error occurred while signing up.");
            setMessageType("error");
        }
    };

    return (
        <div className="profile-container">
            <h2>Create an Account</h2>
            <form onSubmit={handleSubmit} className="signup-form">
                <div className="form-group">
                    <label htmlFor="firstName">First Name:</label>
                    <input
                        type="text"
                        id="firstName"
                        value={firstName}
                        onChange={(e) => setFirstName(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="lastName">Last Name:</label>
                    <input
                        type="text"
                        id="lastName"
                        value={lastName}
                        onChange={(e) => setLastName(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Password:</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" className="submit-btn">Sign Up</button>
            </form>

            {message && (
                <div className={`message ${messageType}`}>
                    {message}
                </div>
            )}
        </div>
    );
};

export default Profile;
