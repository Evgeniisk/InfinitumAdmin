<template>
<h1>At our company security matters</h1>
<div></div>
<h2>Physical Security</h2>
<p>When it comes to cyber security, physical security is the first line of defence.</p>
<p>We have implemented various physical security measures to make sure your data doesn't get corrupted, lost or stolen:</p>
<ul>
    <li>RAID technology to mitigate data loss</li>
    <li>ECC RAM technology to prevent data corruption and/or system failure</li>
    <li>All our servers are located in secure undisclosed locations</li>
    <li>Strict access control measures to our servers and data on them throughout our company</li>
</ul>
<h2>Network Security</h2>
<p>
    We undertand that in the modern world network security matters, which is why we have taken the network security of our web app
    into our own hands.
</p>
<p>
    Instead of using IaaS or PaaS provided by external companies this web application is entirely hosted on my own machine, 
    with network security configured entirely by me.
    I have utilised the latest statuful firewall technology in order to restric internet traffic to our server.
    Additionally I made sure all unnecessary ports on my server machine are closed, and all passwords are at least
    14 characters long and use a combination of uppercase letters, lowercase letters, numbers, and symbols to make
    sure no one can guess our passwords. Additionally we have added security measure to ban ip addresses from connecting to ports
    on our servers for a few hours after some number of failed login attempts preventing brouteforce attacks.
</p>
<h2>Web Security</h2>
<p>This application was designed with security in mind:</p>
<ul>
    <li>All passwords are slated and hashed using well known secure algorithms.</li>
    <li>All data between clients is isolated preventing any data leakage.</li>
    <li>Our web application uses Object Relational Mapping technology which automatically performs database input sanitisation preventing any SQL injection vulnerabilities.</li>
    <li>All user inputted information and files from all user input endpoints are inspected and sanitised preventing cross-site scripting and JavaScript injections.</li>
    <li>Our application implements CSRF token technology to prevent cross-site request forgery.</li>
    <li>Our application uses HTTPS and supports TLSv1.1, TLSv1.2 and TLSv1.3 protocols with various secure cyber suites ensuring availability, confidentiality, integrity, origin authentication, nonrepudiation, entity authentication  </li>
    <li>Additionally we have a digital certificate signed by a reputable certificate authority to prove our identity, intentions and commitment to our clients as a company.</li>
</ul>
</template>

<script lang="ts">

</script>

<style scoped>

</style>