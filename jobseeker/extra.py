      
        {% for form in form_list %}   
                <form action="{% url 'jobseeker:preferred_candidate' job.slug %}" class="form-control" id="preferred_candidate" method="post">
                {% csrf_token %} 
            <div class="container">
                        
                <div class="row">     
                    <tr> 
                        <div class="col-sm-3"> 

                                {% comment %}
                            
                                {% if  field.name == 'profile_photo' %}
                                    <td><img src="{{form.instance.profile_photo.url}}" style="width:60px;height:50px;border-radius:50px;"></td>

                                 {% endcomment %}   

                                {% if field.name == 'name' %}
                                    <td><a href="{% url 'jobseeker:profile' form.instance.slug  %}">{{form.instance.name}}</a></td>   

                                {% elif field.name == 'action_choice' %}
                                    <td>
                                        <select name="selection">
                                            <option value="interested">Interested</option>
                                            <option value="not_interested">Not Interested</option>
                                            <option value="not_answered">Not Answered</option>
                                        </select>

                                    </td>


                                {% comment %}    
                                {% elif field.name == 'current_designation' %}
                                    <td><label>{{form.instance.current_designation.position}}</label></td> 
                                {% elif field.name == 'skills' %}
                                    <td><label>
                                        {% for skill in form.instance.skills.all %}
                                            {{skill.name}}
                                        {% endfor %}
                                    </label></td>  

                                {% else %}
                                    <td><label>{{field.value}}</label></td>
                                {% endif %}

                                {% endcomment %}



                            {% endfor %}

                              <td><button type="submit" class="btn btn-warning">Save</button></td>

                           

                                <td><a href="" class="btn btn-default" data-toggle="modal" data-target="#edit_preferred_candidate">Edit</a></td>

                                {% if form.instance.mail_sent_to_preferred %} 
                                    <td><a href="#" class="btn btn-success disabled ">Send Mail</a></td>
                                {% else %}
                                  <td><a href="{% url 'jobseeker:send_mail' form.instance.slug job.slug %}"data-toggle="modal" data-target="#mail_sent" class="btn btn-success">Send Mail</a></td> 

                              {% endif %}   

                            {% endcomment %}  
                        </div> 
                    </tr>   
                           </div>  
                           
                        {% endfor %}
                    </div> 