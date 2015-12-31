jQuery(function(){
    jQuery.fn.preventDoubleSubmission = function() {
      jQuery(this).on('submit',function(e){
        var the_form = jQuery(this);

        if (the_form.data('submitted') === true) {
          // Previously submitted - don't submit again
          e.preventDefault();
        } else {
          // Mark it so that the next submit can be ignored
          the_form.data('submitted', true);
        }
      });

      // Keep chainability
      return this;
    };
    jQuery('form').preventDoubleSubmission();
});
