<?php

/**
 * Why do we need this at all? Because the Alma Digital manifest service returns a CORS-blocked
 * response when given an MMS ID.
 */


// header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

$id = preg_replace('/[^0-9]/', '', $_GET['id']);

$url = "https://bibsys-k.userservices.exlibrisgroup.com/view/iiif/presentation/${id}/manifest";

echo file_get_contents($url);
