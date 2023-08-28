import { Subject } from "rxjs";
import { BaseIngredient, Ingredient } from "../models/ingredient";
import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Recipe } from "../models/recipe";

@Injectable()
export class RecipesService {
    // to remove later when the endpoint is ready
    private fakeIngredients: BaseIngredient[] = [ 
        { "name": "Farine" },
        { "name": "Sucre" },
        { "name": "Sel" },
        { "name": "Beurre" },
        { "name": "Œufs" },
        { "name": "Lait" },
        { "name": "Levure chimique" },
        { "name": "Huile d'olive" },
        { "name": "Pâtes" },
        { "name": "Riz" },
        { "name": "Céréales" },
        { "name": "Yaourt" },
        { "name": "Fromage" },
        { "name": "Jambon" },
        { "name": "Poulet" },
        { "name": "Thon en conserve" },
        { "name": "Légumes surgelés" },
        { "name": "Fruits frais" },
        { "name": "Café moulu" },
        { "name": "Thé" },
        { "name": "Sucre roux" },
        { "name": "Saumon" },
        { "name": "Salami de boeuf" },
        { "name": "Surimi" },
        { "name": "Sel marin" },
        { "name": "Sole" },
        { "name": "Chocolat noir" },
        { "name": "Épices" }
    ]
    ingredientsSubject: Subject<BaseIngredient[]> = new Subject<BaseIngredient[]>();

    recipe!: Recipe;
    recipeSubject: Subject<Recipe> = new Subject<Recipe>();

    constructor(private http: HttpClient) {}

    loadIngredients(): void {
        // to be modified later when the endpoint is ready
        setTimeout(() => {
            // everybody who's subscribed to the list will be notified
            this.ingredientsSubject.next(this.fakeIngredients.slice());
        }, 1000);
    }

    loadRecipe(selection: Ingredient[]): void {
        const params = {ingredients: selection.map((e) => e.baseIngredient.name)};
        this.http.post<Recipe>('/api/recipe', params).subscribe({
            next: (sentRecipe: Recipe) => {
              this.recipe = sentRecipe;
              this.recipeSubject.next(sentRecipe);
            },
            error: (e) => console.log(e)
        });
    }
}