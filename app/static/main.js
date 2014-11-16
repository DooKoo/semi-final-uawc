function query(city, street, q_type){
    $.post('/query', {city: city, street:street, type:q_type}).done(function(tmp){ $('#result').html(tmp);})
}