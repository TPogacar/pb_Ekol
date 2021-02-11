<!--
	osnovna stran za izpise
-->

% rebase('osnova.tpl', opozorilo=opozorilo)

            <section>
			
				<p>
				<picture><img src="/static/images/EKOL-logo.png" alt="Ekol" height='65' /></picture>
				
			    % import time
					% cas = time.strftime('%d %b %Y ob %Hh %Mmin %Ss', time.localtime())                                                              
			    
				{{cas}}

				
				</p>
				
			</section>

            {{!base}}